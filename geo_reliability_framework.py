"""
Geospatial Insight Reliability Framework (GIRF)
================================================

Judges the RELIABILITY, CONSISTENCY, and CONFIDENCE of insights derived
from multiple space/geospatial data sources (satellite imagery, drones,
IoT/ground sensors, crowdsourced GPS, GIS layers, government datasets, etc).

Design principles
------------------
1. Reliability is a property of the SOURCE (provenance, sensor quality,
   track record) — independent of what any single observation says.
2. Consistency is a property of the EVIDENCE SET — how well independent
   sources agree once aligned in space and time.
3. Confidence is the FUSED output — a single score + interval that
   combines reliability-weighted evidence with the strength of agreement,
   with full traceability back to contributing sources.
4. Every score must be explainable (no black-box single number without
   a breakdown) and updatable (Bayesian feedback from ground truth).

Pipeline
--------
DataSource --> SourceProfiler --(trust_score)-->
Observations --> ConsistencyEngine --(alignment + agreement)-->
Evidence + trust --> ConfidenceFusion --(insight score + CI)-->
InsightEvaluator --> ReliabilityReport (with audit trail)

No third-party dependencies (stdlib only) so it can be dropped into any
pipeline; swap in numpy/scipy/geopandas for production-scale spatial ops.
"""

from __future__ import annotations
import math
import statistics
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# 1. SOURCE MODELING
# ---------------------------------------------------------------------------

class SourceType(Enum):
    SATELLITE = "satellite"
    DRONE_UAV = "drone_uav"
    GROUND_SENSOR = "ground_sensor"
    CROWDSOURCED = "crowdsourced"
    GOVERNMENT_GIS = "government_gis"
    MODEL_DERIVED = "model_derived"  # e.g. another AI model's output


@dataclass
class DataSource:
    """Static + evolving profile of a data source."""
    id: str
    name: str
    type: SourceType
    spatial_resolution_m: float          # lower = better
    temporal_latency_hours: float        # lower = fresher
    sensor_accuracy: float               # 0-1, vendor/spec-sheet accuracy
    provenance_score: float              # 0-1, chain-of-custody / metadata completeness
    # Bayesian track record: Beta(alpha, beta) over "was this source correct
    # when checked against ground truth?"
    accuracy_alpha: float = 2.0
    accuracy_beta: float = 2.0

    @property
    def track_record_accuracy(self) -> float:
        """Posterior mean of historical correctness."""
        return self.accuracy_alpha / (self.accuracy_alpha + self.accuracy_beta)

    @property
    def track_record_confidence(self) -> float:
        """How much evidence backs the track record (more samples = tighter)."""
        n = self.accuracy_alpha + self.accuracy_beta
        return 1 - 1 / math.sqrt(n)  # asymptotically -> 1

    def update_with_ground_truth(self, was_correct: bool) -> None:
        """Bayesian update when a source's claim is later verified."""
        if was_correct:
            self.accuracy_alpha += 1
        else:
            self.accuracy_beta += 1


class SourceProfiler:
    """Computes a single 0-1 trust_score per source from static + learned signals."""

    # Tune these to reflect domain priorities
    WEIGHTS = {
        "sensor_accuracy": 0.30,
        "provenance": 0.20,
        "track_record": 0.35,
        "resolution": 0.15,
    }

    @classmethod
    def trust_score(cls, source: DataSource) -> float:
        # Normalize spatial resolution into a 0-1 "goodness" score
        # (assume anything <=0.5m is excellent, >100m is poor; log-scaled)
        res_score = max(0.0, min(1.0, 1 - math.log10(max(source.spatial_resolution_m, 0.5)) / 2.3))

        # Discount track record by how much evidence backs it
        track_component = source.track_record_accuracy * source.track_record_confidence \
            + 0.5 * (1 - source.track_record_confidence)  # regress to neutral prior if untested

        score = (
            cls.WEIGHTS["sensor_accuracy"] * source.sensor_accuracy +
            cls.WEIGHTS["provenance"] * source.provenance_score +
            cls.WEIGHTS["track_record"] * track_component +
            cls.WEIGHTS["resolution"] * res_score
        )
        return round(max(0.0, min(1.0, score)), 4)


# ---------------------------------------------------------------------------
# 2. OBSERVATIONS (the raw evidence feeding an insight)
# ---------------------------------------------------------------------------

@dataclass
class GeoPoint:
    lat: float
    lon: float

    def haversine_m(self, other: "GeoPoint") -> float:
        R = 6_371_000
        p1, p2 = math.radians(self.lat), math.radians(other.lat)
        dphi = math.radians(other.lat - self.lat)
        dlmb = math.radians(other.lon - self.lon)
        a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
        return 2 * R * math.asin(math.sqrt(a))


@dataclass
class Observation:
    """A single claim from a single source about a location/time, e.g.
    'flood extent = 4.2 sq km' or 'land cover = urban'."""
    source_id: str
    location: GeoPoint
    timestamp: datetime
    value: float | str            # numeric (measurement) or categorical (classification)
    unit: Optional[str] = None
    raw_confidence: Optional[float] = None  # source's own reported confidence, if any


# ---------------------------------------------------------------------------
# 3. CONSISTENCY ENGINE — does independent evidence agree?
# ---------------------------------------------------------------------------

@dataclass
class ConsistencyResult:
    consistency_score: float           # 0-1, agreement among aligned observations
    n_aligned: int
    outliers: list[str]                # source_ids flagged as disagreeing
    detail: str


class ConsistencyEngine:
    def __init__(self, spatial_tolerance_m: float = 500, temporal_tolerance_h: float = 6):
        self.spatial_tolerance_m = spatial_tolerance_m
        self.temporal_tolerance_h = temporal_tolerance_h

    def align(self, observations: list[Observation]) -> list[Observation]:
        """Filter to observations that plausibly refer to the same real-world
        event/location (spatial + temporal clustering around the group centroid)."""
        if not observations:
            return []
        centroid = GeoPoint(
            statistics.mean(o.location.lat for o in observations),
            statistics.mean(o.location.lon for o in observations),
        )
        ref_time = max(o.timestamp for o in observations)
        return [
            o for o in observations
            if o.location.haversine_m(centroid) <= self.spatial_tolerance_m
            and abs((ref_time - o.timestamp).total_seconds()) <= self.temporal_tolerance_h * 3600
        ]

    def score(self, observations: list[Observation]) -> ConsistencyResult:
        aligned = self.align(observations)
        if len(aligned) < 2:
            return ConsistencyResult(0.0, len(aligned), [], "Insufficient independent corroboration.")

        numeric = all(isinstance(o.value, (int, float)) for o in aligned)
        outliers: list[str] = []

        if numeric:
            values = [float(o.value) for o in aligned]
            mean_v, stdev_v = statistics.mean(values), (statistics.stdev(values) if len(values) > 1 else 0.0)
            # Coefficient of variation -> agreement score (low spread = high agreement)
            cv = (stdev_v / abs(mean_v)) if mean_v != 0 else stdev_v
            consistency = max(0.0, 1 - min(cv, 1.0))
            # Flag observations >2 std devs from mean as outliers
            for o in aligned:
                if stdev_v > 0 and abs(float(o.value) - mean_v) > 2 * stdev_v:
                    outliers.append(o.source_id)
            detail = f"Numeric agreement: mean={mean_v:.3f}, stdev={stdev_v:.3f}, CV={cv:.3f}"
        else:
            # Categorical: agreement = majority share; minority = outliers
            counts: dict = {}
            for o in aligned:
                counts[o.value] = counts.get(o.value, 0) + 1
            majority_val, majority_n = max(counts.items(), key=lambda kv: kv[1])
            consistency = majority_n / len(aligned)
            outliers = [o.source_id for o in aligned if o.value != majority_val]
            detail = f"Categorical majority='{majority_val}' ({majority_n}/{len(aligned)} sources agree)"

        return ConsistencyResult(round(consistency, 4), len(aligned), outliers, detail)


# ---------------------------------------------------------------------------
# 4. CONFIDENCE FUSION — combine source trust + consistency + sample size
# ---------------------------------------------------------------------------

@dataclass
class ReliabilityReport:
    insight: str
    confidence_score: float            # 0-1 headline number
    confidence_interval: tuple[float, float]
    reliability_score: float           # weighted avg trust of contributing sources
    consistency_score: float
    n_sources: int
    flagged_outlier_sources: list[str]
    explanation: str
    contributing_sources: list[str]


class ConfidenceFusion:
    def __init__(self, min_sources_for_full_confidence: int = 4):
        self.min_sources_for_full_confidence = min_sources_for_full_confidence

    def fuse(
        self,
        insight: str,
        observations: list[Observation],
        sources: dict[str, DataSource],
        consistency: ConsistencyResult,
    ) -> ReliabilityReport:
        aligned_ids = [o.source_id for o in observations]
        trusts = [SourceProfiler.trust_score(sources[sid]) for sid in aligned_ids if sid in sources]

        reliability = round(statistics.mean(trusts), 4) if trusts else 0.0

        # Sample-size penalty: fewer independent sources -> discount confidence,
        # asymptotically approaching 1 as sources grow.
        sample_factor = min(1.0, consistency.n_aligned / self.min_sources_for_full_confidence)

        # Core fusion: geometric-mean-like combination so a weak link
        # (low reliability OR low consistency) drags confidence down hard,
        # rather than being averaged away.
        confidence = (reliability ** 0.4) * (consistency.consistency_score ** 0.4) * (sample_factor ** 0.2)
        confidence = round(max(0.0, min(1.0, confidence)), 4)

        # Rough uncertainty band: widen interval when sample_factor or
        # consistency is low (more disagreement/fewer sources = more uncertain)
        spread = round(0.25 * (1 - consistency.consistency_score) + 0.15 * (1 - sample_factor), 4)
        ci = (round(max(0.0, confidence - spread), 4), round(min(1.0, confidence + spread), 4))

        explanation = (
            f"{consistency.n_aligned} source(s) corroborate this insight after spatial/temporal "
            f"alignment (mean source reliability={reliability:.2f}, consistency={consistency.consistency_score:.2f}, "
            f"{consistency.detail}). "
            + (f"Outlier source(s) flagged and downweighted: {consistency.outliers}. " if consistency.outliers else "No outliers detected. ")
            + (f"Confidence discounted for limited independent corroboration ({consistency.n_aligned} source(s))."
               if consistency.n_aligned < self.min_sources_for_full_confidence else
               "Sufficient independent corroboration for full confidence weighting.")
        )

        return ReliabilityReport(
            insight=insight,
            confidence_score=confidence,
            confidence_interval=ci,
            reliability_score=reliability,
            consistency_score=consistency.consistency_score,
            n_sources=consistency.n_aligned,
            flagged_outlier_sources=consistency.outliers,
            explanation=explanation,
            contributing_sources=aligned_ids,
        )


# ---------------------------------------------------------------------------
# 5. ORCHESTRATOR
# ---------------------------------------------------------------------------

class InsightEvaluator:
    def __init__(self, spatial_tolerance_m: float = 500, temporal_tolerance_h: float = 6,
                 min_sources_for_full_confidence: int = 4):
        self.consistency_engine = ConsistencyEngine(spatial_tolerance_m, temporal_tolerance_h)
        self.fusion = ConfidenceFusion(min_sources_for_full_confidence)

    def evaluate(self, insight: str, observations: list[Observation], sources: dict[str, DataSource]) -> ReliabilityReport:
        aligned = self.consistency_engine.align(observations)
        consistency = self.consistency_engine.score(observations)
        return self.fusion.fuse(insight, aligned, sources, consistency)

    def record_ground_truth(self, source_id: str, sources: dict[str, DataSource], was_correct: bool) -> None:
        """Feed verified outcomes back in — this is what makes reliability
        scores improve over time rather than being static."""
        if source_id in sources:
            sources[source_id].update_with_ground_truth(was_correct)


# ---------------------------------------------------------------------------
# EXAMPLE USAGE
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    now = datetime.utcnow()

    sources = {
        "sentinel2": DataSource("sentinel2", "Sentinel-2 optical", SourceType.SATELLITE,
                                 spatial_resolution_m=10, temporal_latency_hours=48,
                                 sensor_accuracy=0.9, provenance_score=0.95,
                                 accuracy_alpha=18, accuracy_beta=2),
        "drone_survey": DataSource("drone_survey", "Field drone survey", SourceType.DRONE_UAV,
                                    spatial_resolution_m=0.2, temporal_latency_hours=2,
                                    sensor_accuracy=0.95, provenance_score=0.8,
                                    accuracy_alpha=8, accuracy_beta=1),
        "crowd_reports": DataSource("crowd_reports", "Crowdsourced flood reports", SourceType.CROWDSOURCED,
                                     spatial_resolution_m=200, temporal_latency_hours=0.5,
                                     sensor_accuracy=0.5, provenance_score=0.3,
                                     accuracy_alpha=5, accuracy_beta=5),
        "gov_gis": DataSource("gov_gis", "Municipal flood layer", SourceType.GOVERNMENT_GIS,
                               spatial_resolution_m=30, temporal_latency_hours=24,
                               sensor_accuracy=0.85, provenance_score=0.9,
                               accuracy_alpha=12, accuracy_beta=3),
    }

    observations = [
        Observation("sentinel2", GeoPoint(12.914, 74.856), now - timedelta(hours=1), value=4.1, unit="sq_km"),
        Observation("drone_survey", GeoPoint(12.915, 74.857), now - timedelta(hours=0.5), value=4.4, unit="sq_km"),
        Observation("gov_gis", GeoPoint(12.913, 74.855), now - timedelta(hours=3), value=3.9, unit="sq_km"),
        Observation("crowd_reports", GeoPoint(12.920, 74.860), now - timedelta(hours=0.2), value=9.5, unit="sq_km"),
    ]

    evaluator = InsightEvaluator()
    report = evaluator.evaluate("Flood extent near Mangaluru estuary", observations, sources)

    print(f"Insight: {report.insight}")
    print(f"Confidence: {report.confidence_score} (CI {report.confidence_interval})")
    print(f"Reliability: {report.reliability_score} | Consistency: {report.consistency_score}")
    print(f"Sources: {report.contributing_sources} | Outliers: {report.flagged_outlier_sources}")
    print(f"Explanation: {report.explanation}")