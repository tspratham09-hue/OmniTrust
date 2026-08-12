# engine.py - Advanced OmniTrust Spatial Math Engine
import numpy as np
import hashlib
import json
from datetime import datetime

class OmniTrustEngine:
    def __init__(self):
        # Weights for composite trust score
        self.weights = {"reliability": 0.25, "consistency": 0.25, "confidence": 0.25, "physics": 0.25}

    def compute_reliability(self, sources: dict) -> dict:
        """Calculates sensor decay over time and signal-to-noise ratio."""
        scores = {}
        for name, data in sources.items():
            decay_factor = np.exp(-0.05 * data['freshness_hours'])
            snr_factor = (100 - data['noise_level']) / 100.0
            score = data['quality'] * decay_factor * snr_factor
            scores[name] = float(np.clip(score, 0, 100))
        return scores

    def compute_pairwise_consistency(self, probabilities: list) -> tuple[float, float, np.ndarray]:
        """Calculates full pairwise disagreement matrix using vector operations."""
        probs = np.array(probabilities)
        n = len(probs)
        if n <= 1:
            return 100.0, 0.0, np.zeros((n, n))

        matrix = np.abs(probs[:, None] - probs[None, :]) * 100.0
        triu_indices = np.triu_indices(n, k=1)
        mean_disagreement = np.mean(matrix[triu_indices])
        max_conflict = np.max(matrix[triu_indices])
        
        consistency_score = max(0.0, 100.0 - mean_disagreement)
        return float(consistency_score), float(max_conflict), matrix

    def compute_ensemble_confidence(self, probabilities: list) -> dict:
        """Monte Carlo Ensemble Spread analysis: Confidence = max(0, 1 - 2*std_dev) * 100"""
        probs = np.array(probabilities)
        mean_p = float(np.mean(probs))
        std_dev = float(np.std(probs))
        
        calibrated_confidence = float(np.clip((1.0 - 2.0 * std_dev) * 100.0, 0, 100))
        
        return {
            "mean_p": round(mean_p, 3),
            "std_dev": round(std_dev, 4),
            "confidence_score": round(calibrated_confidence, 1)
        }

    def validate_physics_constraints(self, rainfall_mm: float, slope_deg: float, flood_p: float) -> tuple[float, str]:
        """Hydrological & Slope Rule Enforcement."""
        if flood_p > 0.6 and slope_deg > 25.0 and rainfall_mm < 50.0:
            return 0.25, "PHYSICAL IMPOSSIBILITY: High flood prediction on steep elevation without required runoff precipitation."
        if rainfall_mm > 150.0 and slope_deg < 5.0:
            return 1.0, "PHYSICALLY CONSISTENT: Flat topography combined with heavy rainfall triggers severe accumulation."
        return 1.0, "PHYSICALLY CONSISTENT: Hydrological parameters within valid bounds."

    def generate_audit_hash(self, telemetry_data: dict) -> str:
        """Simulates an immutable blockchain entry by hashing the telemetry state."""
        data_string = json.dumps(telemetry_data, sort_keys=True)
        return hashlib.sha256(data_string.encode()).hexdigest()