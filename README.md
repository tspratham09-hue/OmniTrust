# OmniTrust 🛡️
**Enterprise Verification Layer & Public Safety Navigator for Geospatial AI**

OmniTrust is an advanced geospatial application that shifts the paradigm of navigation from "Fastest Route" to **"Safest Verified Route."** It utilizes a custom Python mathematical engine to actively verify the reliability, consistency, and physics of incoming spatial data feeds, preventing users from being routed into active disaster zones.

## 🚀 Key Features

*   **Real-Time Math Engine:** A custom FastAPI backend computes Monte Carlo ensemble variance, pairwise conflict matrices, and standard deviation spread ($\sigma$) across multiple simulated sensor feeds (Optical, SAR, Weather, Ground).
*   **Dynamic Highway Routing:** Integrates with the OpenStreetMap (Nominatim) and OSRM APIs to generate live, curve-accurate highway routes across India. 
*   **Smart Hazard Avoidance:** Automatically detects hazardous regions and draws verified safe alternative routes, complete with interactive UI hazard pins.
*   **Multi-Modal UI:** Features a custom Map Layer widget (Dark, Street, Satellite, Terrain), live Wikipedia destination image fetching, and multi-vehicle transit time calculations.
*   **Conversational AI Copilot:** A built-in chat widget that can query the Python engine's live telemetry state and answer user safety questions.
*   **Cryptographic Ledger Integration:** Simulates enterprise auditing by generating a live SHA-256 hash of the routing session state.

## 🛠️ Tech Stack

*   **Frontend:** HTML5, Tailwind CSS, JavaScript
*   **Mapping Libraries:** Leaflet.js, MapLibre GL
*   **Backend:** Python 3, FastAPI, Uvicorn, WebSockets
*   **Data Processing:** Numpy, Pandas
*   **Deployment Wrapper:** Streamlit

## 💻 How to Run Locally

Because OmniTrust relies on a real-time mathematical engine, you must run both the backend and frontend servers simultaneously.

1. Clone the repository and install the requirements:
   ```bash
   pip install -r requirements.txt




   
