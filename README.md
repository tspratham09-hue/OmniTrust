# OmniTrust 🛡️

### *Enterprise Geospatial Verification Layer & Public Safety Navigator*

[![Live Demo](https://img.shields.io/badge/Demo-Live%20Streamlit%20App-00D26A?style=for-the-badge&logo=streamlit)](https://omnitrust-yvu8hyvpa7b6mq7nsm5f7f.streamlit.app)
[![Video Demo](https://img.shields.io/badge/Video-Watch%20Walkthrough-FF0000?style=for-the-badge&logo=google-drive)](https://drive.google.com/file/d/18Hjpr2dLB5XN0rAJNy0ekrXDzL18KxwV/view?usp=sharing)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Leaflet](https://img.shields.io/badge/Leaflet-1.9.4-199900?style=for-the-badge&logo=leaflet)](https://leafletjs.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

## 📌 Executive Overview

Traditional geospatial navigation platforms (such as Google Maps, Apple Maps, and Waze) optimize deterministically for **transit speed and shortest distance**. During localized environmental emergencies—such as flash floods, cloudbursts, mudslides, or structural road damage—this logic actively routes unsuspecting motorists directly into hazardous corridors simply because compromised roads exhibit low vehicle density and appear "traffic-free."

Furthermore, legacy crowdsourced hazard systems rely on unverified, anonymous user reports, leaving them susceptible to malicious data spoofing, false alarms, and high noise-to-signal ratios.

**OmniTrust** redefines geospatial mobility from **"Fastest Route"** to **"Safest Verified Route."** Acting as an autonomous **Agentic Verification Engine**, OmniTrust ingests live meteorological telemetry, validates crowdsourced alerts through a **SHA-256 cryptographic audit ledger**, calculates a dynamic mathematical **Trust Score**, and autonomously generates safe geometric detours before commuters arrive at danger zones.

---

## 🏛️ System Architecture


                                  [ User Input / GPS ]
                                            │
                                            ▼
                                 [ OpenStreetMap / OSRM ]
                                            │
                                  (Initial Route Vector)
                                            │
┌───────────────────────────────────────────┴───────────────────────────────────────────┐
│                           OmniTrust Verification Core                                 │
│                                                                                       │
│   ┌─────────────────────┐   ┌───────────────────────┐   ┌─────────────────────────┐   │
│   │   RainViewer API    │   │  Crowdsourced SOS     │   │   Satellite Feeds       │   │
│   │ (Live Doppler Radar)│   │  (Ground Telemetry)   │   │   (SAR & Optical Data)  │   │
│   └──────────┬──────────┘   └───────────┬───────────┘   └────────────┬────────────┘   │
│              │                          │                            │                │
│              └──────────────────┐       │       ┌────────────────────┘                │
│                                 ▼       ▼       ▼                                     │
│                     [ geo_reliability_framework.py ]                                  │
│                      - Monte Carlo Ensemble Variance                                  │
│                      - Pairwise Conflict Matrices                                     │
│                      - Multi-Sensor Consistency Analysis                              │
│                                         │                                             │
│                                         ▼                                             │
│                              [ Dynamic Trust Score ]                                  │
│                                         │                                             │
│                                         ▼                                             │
│                                 [ engine.py ]                                         │
│                      - SHA-256 Cryptographic Audit Ledger                             │
│                      - Physical Anomaly Detection & Geofencing                        │
└─────────────────────────────────────────┬─────────────────────────────────────────────┘
                                          │
                                          ▼
                      [ WebSocket Event Stream (main.py / api.py) ]
                                          │
                   ┌──────────────────────┴──────────────────────┐
                   ▼                                             ▼
        [ Interactive Dashboard ]                     [ Browser Voice AI Copilot ]
        - Dynamic Dark / Street / Satellite           - Web Speech API Synthesis
        - Detour Polyline Overlays                    - Eyes-on-the-Road Audio Prompts
        - Live Crypto Ledger Sync                     - Real-Time Hazard Warnings

## 🚀 Key Features

### 1. 🧮 Mathematical Verification Engine
*   **Ensemble Telemetry Processing:** Continually analyzes data inputs from Optical, Synthetic Aperture Radar (SAR), Weather, and Ground sensor feeds.
*   **Dynamic Trust Scoring:** Computes a composite Trust Metric (0-100) derived from **Reliability**, **Consistency**, **Confidence**, and **Physical Plausibility**.
*   **Hazard Quarantine:** Automatically flags routes whose intersecting hazard probabilities exceed strict safety thresholds.

### 2. 🔐 Cryptographic Audit Ledger
*   **Anti-Spoofing Protocol:** Every crowdsourced hazard report (Flood, Landslide, Crash, Fire) is hashed using **SHA-256** alongside UTC timestamps and coordinate metadata.
*   **Immutable Session State:** Prevents coordinated GPS spoofing and traffic trolling by verifying reports against environmental consensus before allowing topological map alterations.

### 3. 🗺️ Resilient Turn-by-Turn Routing & Detour Generation
*   **OSRM Integration:** Computes curve-accurate highway routing geometries across regional road networks using the Open Source Routing Machine engine.
*   **Autonomous Hazard Geofencing:** If a road segment is flagged hazardous, the engine geofences the node, renders legacy compromised highways as dashed alerts, and plots a verified alternate route in cyan.
*   **Aerial Fallback:** Automatically calculates great-circle aerial interpolation vectors if ground road networks are severed.

### 4. 🎨 Enterprise Multimodal User Interface
*   **Zero-API High-Performance Dark Mode:** Custom dynamic CSS inversion filter over OpenStreetMap tile infrastructure, delivering sleek high-contrast aesthetics without third-party vendor lock-in or watermarks.
*   **Multi-Layer Tile Switcher:** Instant toggling between **Dark Canvas**, **Street View**, **Esri World Imagery (Satellite)**, and **Topographic Terrain**.
*   **Dynamic Transit Computation:** Multi-modal travel time estimation across Driving, Rail, Cycling, and Pedestrian profiles.
*   **Contextual Visuals:** Automated geocoding and real-time Wikipedia image extraction for destination waypoints.

### 5. 🎙️ Browser-Native AI Voice Copilot
*   **Hands-Free Audio Alerts:** Native Web Speech API integration that proactively vocalizes safety updates, route adjustments, and dropping Trust Scores.
*   **Conversational Assistant:** In-app AI agent allowing drivers to query active cryptographic hash records, current system reliability metrics, and safe transit conditions.

---

## 🛠️ Technology Stack

| Domain | Technology / Library | Role in OmniTrust |
| :--- | :--- | :--- |
| **Backend Framework** | **FastAPI / Uvicorn** | High-concurrency asynchronous API routing and execution |
| **Streaming** | **WebSockets** | Sub-millisecond bidirectional telemetry streaming |
| **Frontend UI** | **HTML5, Tailwind CSS, JavaScript** | Responsive glassmorphism interface and interactive sidebars |
| **Mapping Engine** | **Leaflet.js** | Client-side map vector rendering, custom markers, and polylines |
| **Deployment Layer** | **Streamlit Community Cloud** | Microservices hosting and rapid MVP delivery |
| **Geospatial APIs** | **OSRM API & OSM Nominatim** | Turn-by-turn routing geometries and reverse geocoding |
| **Weather Telemetry** | **RainViewer API** | Live Doppler cloud and precipitation radar overlays |
| **Cryptography** | **Python `hashlib` (SHA-256)** | Tamper-evident ledger hashing for hazard verification |
| **Voice Interface** | **Web Speech API** | Browser-native conversational agent and audio alert synthesis |

---

## 📂 Repository Structure


OmniTrust/
├── api.py                      # FastAPI endpoints and route definitions
├── app.py                      # Streamlit application host and entrypoint
├── dashboard.html              # Core Leaflet.js frontend UI, CSS filters & UI logic
├── engine.py                   # Cryptographic ledger hashing & verification pipelines
├── geo_reliability_framework.py # Mathematical Trust Score calculations & physics checks
├── main.py                     # FastAPI WebSocket streaming server
├── requirements.txt            # Python dependencies and library manifests
├── logo                        # Visual brand assets
└── README.md                   # System documentation
