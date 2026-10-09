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

```text
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
