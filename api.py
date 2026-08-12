from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from geo_reliability_framework import DataSource, SourceType, GeoPoint, Observation, InsightEvaluator

app = FastAPI()

# Allow local HTML files to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/evaluate")
def evaluate_insight(optical_quality: float = 0.9):
    now = datetime.utcnow()
    sources = {
        "sentinel2": DataSource("sentinel2", "Sentinel-2", SourceType.SATELLITE, 10, 48, optical_quality, 0.95, 18, 2),
        "drone_survey": DataSource("drone_survey", "Field Drone", SourceType.DRONE_UAV, 0.2, 2, 0.95, 0.8, 8, 1),
    }
    observations = [
        Observation("sentinel2", GeoPoint(12.914, 74.856), now - timedelta(hours=1), value=4.1, unit="sq_km"),
        Observation("drone_survey", GeoPoint(12.915, 74.857), now - timedelta(hours=0.5), value=4.4, unit="sq_km"),
    ]

    evaluator = InsightEvaluator()
    report = evaluator.evaluate("Flood extent near Mangaluru estuary", observations, sources)

    return {
        "confidence_score": int(report.confidence_score * 100),
        "reliability_score": int(report.reliability_score * 100),
        "consistency_score": int(report.consistency_score * 100),
        "explanation": report.explanation
    }