# PRAVAH-NER — Development Setup

This guide explains how to set up the **PRAVAH-NER** project locally using **uv**, Python 3.12, JupyterLab, and the project's development dependencies.

PRAVAH-NER is an AI-powered logistics intelligence platform for predicting road disruptions, monitoring road accessibility, and optimizing transportation routes across Northeast India.

---

# 1. Prerequisites

Make sure the following are installed:

* Git
* Python 3.12
* uv
* Microsoft C++ Build Tools *(Windows users — required by Pyrosm/cykhash)*

Check the installations:

```bash
git --version
python --version
uv --version
```

The project currently uses:

```text
Python 3.12.x
```

> **Why Python 3.12?**
>
> PRAVAH-NER uses geospatial packages such as Pyrosm and its native dependency `cykhash`. Python 3.12 provides better compatibility for the current GIS stack than Python 3.13.

---

# 2. Install uv

If `uv` is not installed, follow the official installation guide:

[uv Installation Guide](https://docs.astral.sh/uv/getting-started/installation/?utm_source=chatgpt.com)

Verify:

```bash
uv --version
```

---

# 3. Install Python 3.12 using uv

Install Python 3.12:

```bash
uv python install 3.12
```

Pin Python 3.12 for the project:

```bash
uv python pin 3.12
```

This creates:

```text
.python-version
```

containing:

```text
3.12
```

Verify:

```bash
uv run python --version
```

Expected:

```text
Python 3.12.x
```

> **Important:** `uv python pin 3.12` does not change an already-created virtual environment. If `.venv` was previously created using Python 3.13, delete and recreate it.

---

# 4. Windows — Microsoft C++ Build Tools

PRAVAH-NER uses **Pyrosm** for processing OpenStreetMap `.osm.pbf` files.

Pyrosm depends on native packages such as:

```text
Pyrosm
   ↓
cykhash
   ↓
C/C++ extension
```

On Windows, `cykhash` may need to be compiled locally.

If you encounter:

```text
error: Microsoft Visual C++ 14.0 or greater is required
```

install:

[Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/?utm_source=chatgpt.com)

During installation select:

```text
Desktop development with C++
```

The installation should include:

* MSVC C++ build tools
* Windows SDK
* C++ build tools

You do **not** need the full Visual Studio IDE.

After installation, restart your terminal.

---

# 5. Clone the Repository

```bash
git clone <REPOSITORY_URL>

cd PRAVAH-NER
```

---

# 6. Project Structure

The project is organized into backend, ML, frontend, data, and infrastructure components.

```text
PRAVAH-NER/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── logging.py
│   │   │   └── exceptions.py
│   │   │
│   │   ├── api/
│   │   │   ├── dependencies.py
│   │   │   └── v1/
│   │   │       ├── router.py
│   │   │       ├── auth.py
│   │   │       ├── roads.py
│   │   │       ├── risks.py
│   │   │       ├── incidents.py
│   │   │       ├── routes.py
│   │   │       ├── shipments.py
│   │   │       ├── alerts.py
│   │   │       └── health.py
│   │   │
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── risk/
│   │   │   ├── routing/
│   │   │   ├── incidents/
│   │   │   ├── shipments/
│   │   │   ├── alerts/
│   │   │   └── data/
│   │   │
│   │   ├── repositories/
│   │   ├── db/
│   │   └── integrations/
│   │       ├── weather/
│   │       ├── routing/
│   │       ├── ml/
│   │       └── notifications/
│   │
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── api/
│   │
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── uv.lock
│   └── Dockerfile
│
├── ml/
│   ├── datasets/
│   │   ├── raw/
│   │   ├── processed/
│   │   └── README.md
│   │
│   ├── notebooks/
│   │   ├── 01_data_exploration.ipynb
│   │   ├── 02_road_network.ipynb
│   │   ├── 03_feature_engineering.ipynb
│   │   ├── 04_risk_model.ipynb
│   │   └── 05_model_evaluation.ipynb
│   │
│   ├── training/
│   │   ├── train.py
│   │   ├── evaluate.py
│   │   └── features.py
│   │
│   ├── models/
│   │   └── blockage_model/
│   │
│   └── inference/
│       └── predictor.py
│
├── frontend/
│
├── data/
│   ├── sample/
│   └── seed/
│
├── infrastructure/
│   ├── docker/
│   ├── nginx/
│   └── monitoring/
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

> `.venv/` must **never** be committed to Git.

---

# 7. Backend Setup

Navigate to the backend:

```bash
cd backend
```

---

## 7.1 Create the Virtual Environment

Use uv:

```bash
uv venv
```

This creates:

```text
backend/
└── .venv/
```

Because Python 3.12 is pinned, uv will use Python 3.12 for the environment.

Verify:

```bash
uv run python --version
```

Expected:

```text
Python 3.12.x
```

---

# 8. Activate the Virtual Environment

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows CMD

```cmd
.venv\Scripts\activate.bat
```

### Linux / macOS

```bash
source .venv/bin/activate
```

After activation:

```text
(.venv) PS C:\...\PRAVAH-NER\backend>
```

> Activation is optional when using `uv run`.

---

# 9. Install Dependencies

PRAVAH-NER uses `uv` for dependency management.

If the project already contains:

```text
pyproject.toml
uv.lock
```

run:

```bash
uv sync
```

This installs the locked dependencies.

---

## Installing from requirements.txt

If dependencies are maintained in `requirements.txt`, they can be installed using:

```bash
uv pip install -r requirements.txt
```

However, the preferred long-term approach for this project is:

```text
pyproject.toml
        +
uv.lock
```

rather than maintaining two independent dependency sources.

---

# 10. Current Python Dependencies

The project currently uses or plans to use the following Python libraries:

### Backend / API

```text
fastapi
uvicorn
pydantic
pydantic-settings
```

### GIS / Geospatial

```text
geopandas
pyrosm
shapely
pyproj
fiona
```

### Graph / Routing

```text
networkx
```

### Machine Learning / Data Science

```text
numpy
pandas
scikit-learn
xgboost
joblib
```

### External APIs

```text
httpx
```

### Database

```text
sqlalchemy
asyncpg
geoalchemy2
alembic
```

### Environment Configuration

```text
python-dotenv
```

### Jupyter / ML Development

```text
jupyterlab
ipykernel
```

### Testing

```text
pytest
pytest-asyncio
```

### Code Quality

```text
ruff
```

---

# 11. Jupyter Notebook Setup

Jupyter is used primarily for the **ML, GIS, data exploration, and experimentation workflow**.

Install JupyterLab and the kernel:

```bash
uv add --dev jupyterlab ipykernel
```

Register the project environment as a Jupyter kernel:

```bash
uv run python -m ipykernel install --user --name pravah-ner --display-name "PRAVAH-NER"
```

Start JupyterLab:

```bash
uv run jupyter lab
```

Then select:

```text
Kernel → Change Kernel → PRAVAH-NER
```

---

# 12. Notebook Development Workflow

The ML development process should follow:

```text
Raw Data
   ↓
Data Exploration
   ↓
Data Cleaning
   ↓
Feature Engineering
   ↓
Model Training
   ↓
Model Evaluation
   ↓
Model Selection
   ↓
Model Export
   ↓
Inference
```

Example notebook organization:

```text
ml/notebooks/

01_data_exploration.ipynb
02_road_network.ipynb
03_feature_engineering.ipynb
04_risk_model.ipynb
05_model_evaluation.ipynb
```

Notebooks should primarily be used for:

* experimentation
* visualization
* data analysis
* model experimentation
* debugging ideas

Final reusable logic should be moved into Python modules.

---

# 13. Run the Backend

Start the FastAPI development server:

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# 14. Verify the Installation

Test the health endpoint:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{
    "status": "healthy"
}
```

Terminal:

```bash
curl http://127.0.0.1:8000/health
```

---

# 15. Verify Important Dependencies

After installation, verify the GIS stack:

```bash
uv run python -c "import pyrosm; print('Pyrosm OK')"
```

```bash
uv run python -c "import geopandas; print('GeoPandas OK')"
```

```bash
uv run python -c "import networkx; print('NetworkX OK')"
```

Verify ML:

```bash
uv run python -c "import sklearn; print('Scikit-learn OK')"
```

```bash
uv run python -c "import xgboost; print('XGBoost OK')"
```

Verify Jupyter:

```bash
uv run jupyter --version
```

---

# 16. Dependency Management

## Add a dependency

```bash
uv add <package>
```

Example:

```bash
uv add networkx
```

---

## Add a development dependency

```bash
uv add --dev <package>
```

Example:

```bash
uv add --dev pytest
```

---

## Remove a dependency

```bash
uv remove <package>
```

Example:

```bash
uv remove networkx
```

---

## Synchronize dependencies

Whenever dependencies or the repository are updated:

```bash
uv sync
```

---

## Run commands through uv

You don't need to manually activate `.venv`.

For example:

```bash
uv run uvicorn app.main:app --reload
```

or:

```bash
uv run pytest
```

or:

```bash
uv run python script.py
```

---

# 17. Environment Variables

PRAVAH-NER will use environment variables for API keys and configuration.

Create:

```text
backend/
└── .env
```

Example:

```env
APP_ENV=development

WEATHER_API_KEY=

DATABASE_URL=

GPS_API_KEY=
```

Never commit `.env` to Git.

The `.gitignore` should contain:

```gitignore
.env
.env.*
!.env.example

.venv/

__pycache__/
*.py[cod]

.ipynb_checkpoints/

# ML / GIS datasets
ml/datasets/raw/
ml/datasets/processed/

# Large OSM files
*.osm.pbf

# Trained model artifacts
# Uncomment if models should not be version controlled
# ml/models/

# Build artifacts
build/
dist/
*.egg-info/
```

---

# 18. Planned Technology Stack

| Component          | Technology             |
| ------------------ | ---------------------- |
| API                | FastAPI                |
| Language           | Python 3.12            |
| Package Management | uv                     |
| Notebook           | JupyterLab             |
| Road Network       | OpenStreetMap          |
| OSM Processing     | Pyrosm                 |
| GIS                | GeoPandas              |
| Spatial Database   | PostgreSQL + PostGIS   |
| Graph              | NetworkX               |
| Routing            | Dijkstra / A*          |
| ML                 | Scikit-learn / XGBoost |
| Weather            | Weather API            |
| Vehicle Tracking   | GPS                    |
| Frontend           | React + TypeScript     |
| Map                | MapLibre               |
| Containerization   | Docker                 |

Dependencies will be added **incrementally** as each subsystem is implemented.

---

# 19. Development Workflow

The overall development flow is:

```text
Clone Repository
       ↓
Set Python 3.12
       ↓
Create / Sync uv Environment
       ↓
Install Dependencies
       ↓
Run FastAPI
       ↓
Develop API
       ↓
Add GIS Pipeline
       ↓
Download OSM Data
       ↓
Build Road Network
       ↓
Build Graph
       ↓
Dijkstra / A*
       ↓
Add Weather & Incident Data
       ↓
Train Risk Model
       ↓
Calculate Dynamic Edge Weights
       ↓
Risk-Aware Routing
       ↓
ETA / Delay Prediction
       ↓
React + MapLibre Dashboard
```

---

# 20. GIS Data Setup

The road network will initially be based on **OpenStreetMap** data.

Typical pipeline:

```text
.osm.pbf
    ↓
Pyrosm
    ↓
GeoDataFrame
    ↓
Road Segments
    ↓
NetworkX Graph
```

Regional OSM data can be obtained from providers such as Geofabrik.

Large `.osm.pbf` files should **not** be committed to Git.

Recommended:

```text
ml/datasets/raw/
```

for local/raw data.

---

# 21. Machine Learning Setup

The initial ML system focuses on:

> **Road disruption/blockage risk prediction.**

The initial pipeline:

```text
Weather
Road Condition
Terrain
Historical Incidents
Traffic
       ↓
Feature Engineering
       ↓
ML Model
       ↓
Disruption Probability
       ↓
Road Risk Score
```

Example output:

```text
Risk Probability = 0.82
Risk Level = HIGH
Confidence = 0.91
```

The predicted risk will influence the routing engine.

```text
Risk Score
    ↓
Dynamic Edge Weight
    ↓
Dijkstra / A*
    ↓
Risk-Aware Route
```

---

# 22. Routing Model

The transportation network is represented as a graph:

```text
Nodes = intersections / locations

Edges = road segments
```

The routing engine will initially support:

```text
Dijkstra
A*
```

The edge cost should consider more than distance.

Initial conceptual formula:

```text
Edge Cost =
Travel Time ×
(1 + α × Risk + β × Congestion)
```

If a road is confirmed blocked:

```text
Edge Cost = ∞
```

The routing engine can therefore avoid dangerous or inaccessible roads.

---

# 23. Common Commands

### Start backend

```bash
uv run uvicorn app.main:app --reload
```

### Synchronize dependencies

```bash
uv sync
```

### Add package

```bash
uv add <package>
```

### Add development package

```bash
uv add --dev <package>
```

### Run tests

```bash
uv run pytest
```

### Check code quality

```bash
uv run ruff check .
```

### Start JupyterLab

```bash
uv run jupyter lab
```

### Check Python version

```bash
uv run python --version
```

---

# 24. Contribution Workflow

Create a feature branch:

```bash
git checkout -b feature/<feature-name>
```

Example:

```bash
git checkout -b feature/road-network
```

After making changes:

```bash
git add .
git commit -m "feat: add road network processing"
git push origin feature/road-network
```

Create a Pull Request after pushing the branch.

---

# 25. Current Development Status

PRAVAH-NER is currently under active development.

Initial development priorities:

```text
[x] Project structure
[x] uv environment
[x] Python 3.12
[x] Jupyter development environment
[ ] FastAPI backend
[ ] OpenStreetMap road extraction
[ ] Road graph construction
[ ] Basic Dijkstra/A* routing
[ ] Weather integration
[ ] Incident data pipeline
[ ] ML risk prediction
[ ] Dynamic edge weighting
[ ] ETA prediction
[ ] Vehicle tracking
[ ] React + MapLibre dashboard
```

---

# 26. Important Development Rules

### 1. Use Python 3.12

The current project environment is standardized on Python 3.12.

### 2. Use uv

Use `uv` for environment and dependency management.

Prefer:

```bash
uv add <package>
```

over manually installing packages with pip.

### 3. Don't commit `.venv`

```text
.venv/
```

must remain in `.gitignore`.

### 4. Don't commit large datasets

Do not commit:

```text
*.osm.pbf
```

or large raw datasets.

### 5. Don't put production logic in notebooks

Use notebooks for experimentation.

Move finalized code into:

```text
ml/training/
ml/inference/
backend/app/services/
```

### 6. Add dependencies incrementally

Do not install every planned dependency before the corresponding subsystem is implemented.

---

# 27. Current Architecture

The core PRAVAH-NER pipeline is:

```text
                ROAD NETWORK
                     │
                     ▼
            Weather / Incidents
                     │
                     ▼
              Risk Prediction
                     │
                     ▼
             Road Accessibility
                     │
                     ▼
              Dynamic Edge Cost
                     │
                     ▼
                Dijkstra / A*
                     │
                     ▼
               Optimal Route
                     │
                     ▼
                 ETA / Delay
                     │
                     ▼
              FastAPI Backend
                     │
                     ▼
             React + MapLibre
                     │
                     ▼
            PRAVAH-NER Dashboard
```

The central objective is:

> **Find a practical route that balances travel time, accessibility, congestion, and disruption risk rather than simply selecting the shortest route.**

---

# 28. Troubleshooting

## `Microsoft Visual C++ 14.0 or greater is required`

If you see:

```text
error: Microsoft Visual C++ 14.0 or greater is required
```

this usually occurs while building:

```text
cykhash
```

which is required by:

```text
pyrosm
```

On Windows, install:

**Desktop development with C++**

from Microsoft's Build Tools installer.

After installation:

1. Close the terminal.
2. Open a new terminal.
3. Activate the environment if necessary.
4. Run:

```bash
uv sync
```

Then verify:

```bash
uv run python -c "import pyrosm; print('Pyrosm OK')"
```

---

## Python version shows 3.13 after `uv python pin 3.12`

`uv python pin 3.12` only changes the project's Python version preference.

If an existing `.venv` was created with Python 3.13, recreate it:

```powershell
deactivate
Remove-Item -Recurse -Force .venv
uv sync
```

Verify:

```powershell
uv run python --version
```

Expected:

```text
Python 3.12.x
```

---

# 29. Deployment Consideration

Some PRAVAH-NER dependencies contain native C/C++ components.

For example:

```text
Pyrosm
   ↓
cykhash
   ↓
native C/C++ extension
```

This is primarily a **build-time requirement**.

For deployment, PRAVAH-NER should preferably use Docker so that the required system dependencies can be installed during the image build.

Conceptually:

```text
Dockerfile
    ↓
Linux build environment
    ↓
Install native build dependencies
    ↓
Install Python dependencies
    ↓
Build application image
    ↓
Deploy container
```

This provides a reproducible environment between development and deployment.

---

# 30. Development Philosophy

PRAVAH-NER should be developed incrementally.

Do not attempt to build the entire system simultaneously.

Start with:

```text
Road Network
     ↓
Graph
     ↓
Routing
```

Then introduce:

```text
Weather
     +
Incidents
     ↓
Risk
```

Then:

```text
Risk
     +
Travel Time
     +
Congestion
     ↓
Dynamic Routing
```

Finally integrate:

```text
FastAPI
     +
ML
     +
GIS
     +
React
     +
MapLibre
```

This approach allows every subsystem to be tested independently before being integrated into the complete platform.
