# PRAVAH-NER

### Predictive Regional Accessibility & Logistics Intelligence

> **AI-powered logistics intelligence for safer, smarter, and more resilient transportation across Northeast India.**

PRAVAH-NER is an AI-powered logistics and road accessibility intelligence platform designed to address transportation challenges in India's North Eastern Region (NER), where difficult terrain, extreme weather, landslides, floods, road damage, and limited connectivity can significantly disrupt the movement of essential goods.

The platform combines **GIS, road-network analysis, weather intelligence, incident data, machine learning, graph algorithms, and real-time logistics information** to predict road disruptions and identify safer and more efficient transportation routes.

---

## Problem

The North Eastern Region faces unique transportation challenges:

* Difficult and mountainous terrain
* Heavy rainfall and extreme weather
* Landslides and flooding
* Road and bridge damage
* Limited connectivity to remote areas
* Delays in transportation of essential goods
* Lack of centralized road accessibility intelligence
* Limited real-time visibility of logistics operations

A road that is geographically shorter is not necessarily the best route.

For example:

```text
Route A
Distance: 80 km
Travel time: 2 hours
Risk: LOW
        ↓
     Preferred

Route B
Distance: 65 km
Travel time: 1.5 hours
Risk: HIGH
        ↓
     Avoid
```

PRAVAH-NER aims to make routing decisions based not only on distance or travel time, but also on **current and predicted road risk**.

---

# Solution

PRAVAH-NER follows a risk-aware logistics pipeline:

```text
                    ┌──────────────────┐
                    │  Road Network    │
                    │ OpenStreetMap    │
                    └────────┬─────────┘
                             │
                             ▼
                 ┌──────────────────────┐
                 │ Weather & Incidents  │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Risk Prediction    │
                 │      ML Model        │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Road Accessibility   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Dynamic Edge Cost    │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    Dijkstra / A*     │
                 │  Route Optimization  │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    ETA / Delay       │
                 └──────────────────────┘
```

---

# Core Features

### 🗺️ Road Accessibility Monitoring

Monitor road segments and determine their current accessibility status.

Possible states include:

```text
🟢 OPEN
🟡 AT RISK
🟠 RESTRICTED
🔴 BLOCKED
```

---

### 🌧️ Weather-Based Risk Analysis

Weather conditions can influence road accessibility.

Relevant factors may include:

* Rainfall
* Heavy rainfall events
* Flood conditions
* Temperature
* Weather warnings
* Historical weather patterns

---

### 🤖 AI-Based Risk Prediction

The ML layer predicts the probability of disruption for a road segment.

Example:

```text
Road Segment: NH-XX

Rainfall        → 145 mm
Slope           → 31°
Historical risk → High
Current incident→ Landslide

                ↓

Disruption Probability
        0.82

                ↓

Risk Level
        HIGH
```

---

### 🛣️ Risk-Aware Route Optimization

Instead of optimizing only for shortest distance, PRAVAH-NER considers multiple factors.

Conceptually:

```text
Travel Time
     +
Disruption Risk
     +
Congestion
     ↓
Generalized Edge Cost
     ↓
Dijkstra / A*
     ↓
Optimal Route
```

A blocked road is excluded from route computation.

---

### 🚚 Logistics & Shipment Tracking

The platform is designed to support tracking of vehicles transporting:

* Medicines
* Food supplies
* Agricultural products
* Construction materials
* Emergency supplies

GPS information can be used to monitor:

```text
Vehicle
   ↓
Current Location
   ↓
Current Route
   ↓
Destination
   ↓
ETA
```

---

### 🚨 Incident Management

Field officials can report incidents such as:

* Landslides
* Floods
* Road damage
* Bridge damage
* Accidents
* Traffic blockages

Reports can contain:

```text
Incident
├── Location
├── Timestamp
├── Type
├── Severity
├── Description
└── Photograph
```

---

### 🔔 Alerts

The platform can generate alerts for:

* Road blockages
* High-risk corridors
* Predicted disruptions
* Delayed shipments
* Inaccessible regions
* Emergency route changes

---

### 📊 Intelligence Dashboard

The web dashboard is designed to provide centralized visibility of:

* District connectivity
* Road accessibility
* Risk zones
* Logistics bottlenecks
* Active incidents
* Vehicle locations
* Emergency routes
* Shipment status

---

# System Architecture

```text
                         PRAVAH-NER
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
     Frontend              Backend                 ML
        │                     │                     │
   React + MapLibre        FastAPI             Risk Model
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                         Data Layer
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
     Road Network          Weather            Incidents
     OpenStreetMap           API             Field Reports
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
                              ▼
                       PostgreSQL/PostGIS
```

---

# Routing Architecture

The routing engine represents the road network as a graph.

```text
Road Network
     ↓
Graph
     ↓
Nodes + Edges
     ↓
Edge Attributes
     │
     ├── Distance
     ├── Travel Time
     ├── Risk
     ├── Accessibility
     └── Congestion
     ↓
Dynamic Edge Cost
     ↓
Dijkstra / A*
     ↓
Optimal Route
```

### Edge Cost

The initial routing model uses a generalized edge cost:

```text
Edge Cost =
Travel Time ×
(1 + Risk Penalty + Congestion Penalty)
```

For a blocked road:

```text
Edge Cost = ∞
```

This allows the routing algorithm to automatically avoid inaccessible roads.

The cost function will be refined and calibrated as historical data becomes available.

---

# Machine Learning Pipeline

The initial ML objective is **road disruption/blockage risk prediction**.

```text
Raw Data
   ↓
Data Cleaning
   ↓
Feature Engineering
   ↓
Training Dataset
   ↓
ML Model
   ↓
Evaluation
   ↓
Saved Model
   ↓
Inference
   ↓
Risk Probability
```

Potential features include:

```text
Weather
├── Rainfall
├── Rainfall intensity
└── Weather conditions

Terrain
├── Elevation
├── Slope
└── Terrain characteristics

Road
├── Road type
├── Road condition
└── Historical accessibility

Incidents
├── Landslides
├── Floods
├── Accidents
└── Road damage
```

The model produces a disruption probability:

```text
0.00 ───────────────────────────── 1.00
 LOW                MEDIUM              HIGH
```

---

# Technology Stack

## Backend

* Python
* FastAPI
* Pydantic

## Geospatial

* OpenStreetMap
* Pyrosm
* GeoPandas
* PostGIS

## Graph & Routing

* NetworkX
* Dijkstra
* A*

## Machine Learning

* Scikit-learn
* XGBoost

## Frontend

* React
* TypeScript
* MapLibre

## Database

* PostgreSQL
* PostGIS

## Development

* uv
* Git
* Docker

---

# Repository Structure

```text
├── backend/
│ ├── app/
│ │ ├── main.py
│ │ │
│ │ ├── core/
│ │ │ ├── config.py
│ │ │ ├── security.py
│ │ │ ├── logging.py
│ │ │ └── exceptions.py
│ │ │
│ │ ├── api/
│ │ │ ├── dependencies.py
│ │ │ └── v1/
│ │ │ ├── router.py
│ │ │ ├── auth.py
│ │ │ ├── roads.py
│ │ │ ├── risks.py
│ │ │ ├── incidents.py
│ │ │ ├── routes.py
│ │ │ ├── shipments.py
│ │ │ ├── alerts.py
│ │ │ └── health.py
│ │ │
│ │ ├── models/
│ │ │ ├── user.py
│ │ │ ├── road.py
│ │ │ ├── risk.py
│ │ │ ├── incident.py
│ │ │ ├── shipment.py
│ │ │ ├── route.py
│ │ │ └── alert.py
│ │ │
│ │ ├── schemas/
│ │ │ ├── road.py
│ │ │ ├── risk.py
│ │ │ ├── incident.py
│ │ │ ├── shipment.py
│ │ │ ├── route.py
│ │ │ └── alert.py
│ │ │
│ │ ├── services/
│ │ │ ├── risk/
│ │ │ │ ├── risk_engine.py
│ │ │ │ ├── risk_calculator.py
│ │ │ │ └── confidence.py
│ │ │ │
│ │ │ ├── routing/
│ │ │ │ ├── routing_engine.py
│ │ │ │ ├── graph.py
│ │ │ │ └── cost_function.py
│ │ │ │
│ │ │ ├── incidents/
│ │ │ ├── shipments/
│ │ │ ├── alerts/
│ │ │ └── data/
│ │ │
│ │ ├── repositories/
│ │ │ ├── road_repository.py
│ │ │ ├── risk_repository.py
│ │ │ ├── incident_repository.py
│ │ │ ├── shipment_repository.py
│ │ │ └── route_repository.py
│ │ │
│ │ ├── db/
│ │ │ ├── database.py
│ │ │ ├── session.py
│ │ │ └── migrations/
│ │ │
│ │ └── integrations/
│ │ ├── weather/
│ │ ├── routing/
│ │ ├── ml/
│ │ └── notifications/
│ │
│ ├── tests/
│ │ ├── unit/
│ │ ├── integration/
│ │ └── api/
│ │
│ ├── requirements.txt
│ └── Dockerfile
│
├── ml/
│ ├── datasets/
│ │ ├── raw/
│ │ ├── processed/
│ │ └── README.md
│ │
│ ├── notebooks/
│ ├── training/
│ │ ├── train.py
│ │ ├── evaluate.py
│ │ └── features.py
│ │
│ ├── models/
│ │ └── blockage_model/
│ │
│ ├── inference/
│ │ └── predictor.py
│ └── requirements.txt
│
├── frontend/
├── data/
│ ├── sample/
│ └── seed/
│
├── infrastructure/
│ ├── docker/
│ ├── nginx/
│ └── monitoring/
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

# Development Roadmap

## Phase 1 — Project Foundation

* [x] Repository initialization
* [x] Python environment with uv
* [ ] FastAPI application
* [ ] Configuration management
* [ ] Logging
* [ ] Basic health endpoint

## Phase 2 — Road Network

* [ ] Obtain OpenStreetMap data
* [ ] Process `.osm.pbf` data
* [ ] Extract road network
* [ ] Convert roads into graph
* [ ] Store geospatial data

## Phase 3 — Routing Engine

* [ ] Implement graph representation
* [ ] Implement Dijkstra
* [ ] Implement A*
* [ ] Calculate travel-time cost
* [ ] Handle blocked roads
* [ ] Implement dynamic edge weights

## Phase 4 — Risk Intelligence

* [ ] Collect weather data
* [ ] Collect historical incident data
* [ ] Feature engineering
* [ ] Train blockage-risk model
* [ ] Evaluate model
* [ ] Build inference pipeline

## Phase 5 — Dynamic Routing

```text
Weather
   +
Incidents
   +
ML Risk
   ↓
Updated Edge Weights
   ↓
Dijkstra / A*
   ↓
Risk-Aware Route
```

* [ ] Integrate risk model with routing
* [ ] Implement alternate routes
* [ ] Estimate route delay
* [ ] Compare route alternatives

## Phase 6 — Logistics

* [ ] Shipment management
* [ ] Vehicle tracking
* [ ] GPS integration
* [ ] ETA calculation
* [ ] Delivery status

## Phase 7 — Intelligence Dashboard

* [ ] Interactive map
* [ ] Road accessibility layer
* [ ] Risk visualization
* [ ] Incident visualization
* [ ] Vehicle tracking
* [ ] Shipment dashboard
* [ ] Alerts

## Phase 8 — Production

* [ ] Authentication
* [ ] Role-based access
* [ ] Dockerization
* [ ] Database migrations
* [ ] Monitoring
* [ ] Security hardening
* [ ] Offline synchronization
* [ ] Multilingual notifications

---

# Development Setup

See [SETUP.md](SETUP.md) for complete local development instructions.

Quick start:

```bash
uv sync
```

Run the backend:

```bash
uv run uvicorn app.main:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Data Sources

The project is designed to integrate multiple data sources.

### Road Network

**OpenStreetMap** provides the initial road-network data.

```text
.osm.pbf
   ↓
Pyrosm
   ↓
Road segments
   ↓
Graph
```

### Weather

Weather APIs can provide:

* Rainfall
* Temperature
* Weather conditions
* Forecasts
* Severe weather information

### Incident Data

Potential sources include:

* Government/open datasets
* Historical disaster records
* Field reports
* Road authority reports
* Manually generated incident data for prototype development

### Terrain

Potential geospatial features include:

* Elevation
* Slope
* Terrain characteristics

---

# Design Philosophy

PRAVAH-NER is built around one central idea:

> **The shortest route is not always the safest or most accessible route.**

The platform therefore combines:

```text
Distance
+
Travel Time
+
Weather
+
Terrain
+
Incidents
+
Predicted Risk
+
Accessibility
```

to produce a more practical route for real-world logistics operations.

---

# Project Status

🚧 **Early Development**

The project is currently being developed incrementally, beginning with the backend foundation and road-network/routing infrastructure.

Features listed in the roadmap may not yet be implemented.

---

# License

License information will be added as the project matures.
