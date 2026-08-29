```markdown
# How to Run Pravah Backend Locally

This guide will help you set up and run the Pravah Logistics Intelligence backend on your own machine. It assumes you are using Docker for the database and Python for the FastAPI server.

---

## Prerequisites

Make sure you have the following installed:

- **Git** – [Download](https://git-scm.com/)
- **Docker** – [Download](https://docs.docker.com/get-docker/)
- **Docker Compose** – included with Docker Desktop, or install separately on Linux
- **Python 3.10+** – [Download](https://www.python.org/downloads/)
- **pip** – usually comes with Python

---

## 1. Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/SigmaSharmaG/Pravah.git
cd Pravah
```

---

## 2. Environment Configuration

The backend reads configuration from environment variables. A sample file `.env.example` may be provided. Create your own `.env` file:

```bash
cp .env.example .env
```

Open `.env` and update the values if needed. For local development, the defaults should work:

```
DATABASE_URL=postgresql://pravah:pravah123@localhost:5432/pravah_db
OSRM_URL=http://router.project-osrm.org
SECRET_KEY=your-secret-key-change-this
```

**Important:** The `DATABASE_URL` must match the credentials used in `docker-compose.yml` (see next step).

---

## 3. Start PostgreSQL with Docker Compose

The repository includes a `docker-compose.yml` file that sets up a PostgreSQL database with PostGIS.

Run:

```bash
docker-compose up -d db
```

This will pull the `postgis/postgis:15-3.3` image and start a container named `pravah-db-1` (or similar).

Check that the container is running:

```bash
docker ps
```

Wait a few seconds for the database to initialize.

---

## 4. Enable PostGIS Extensions

The PostGIS image does **not** automatically create the `postgis` extension in your database. You must do it manually.

Connect to the database inside the container:

```bash
docker exec -it <container_name> psql -U pravah -d pravah_db
```

Replace `<container_name>` with the actual container name (e.g., `pravah-db-1`). You can find it with `docker ps`.

Once inside the `psql` shell, run:

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
```

Exit with `\q`.

> **Note:** If you later recreate the database volume, you will need to run these commands again. Alternatively, you can place these commands in a SQL initialization script mounted into `/docker-entrypoint-initdb.d/` in the container.

---

## 5. Install Python Dependencies

Navigate to the `backend/` folder:

```bash
cd backend
```

Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not yet complete, ensure at least these are installed:

```bash
pip install fastapi uvicorn sqlalchemy geoalchemy2 psycopg2-binary alembic pydantic python-dotenv shapely pyproj
```

---

## 6. (Optional) Load Sample Road Data

To test the API with some road segments, you can load sample data from a GeoJSON file or use the provided script.

If you have a GeoJSON file (e.g., downloaded from Overpass Turbo), place it in `backend/data/roads.geojson`. Then run:

```bash
python scripts/load_geojson_roads.py data/roads.geojson
```

Alternatively, you can generate synthetic terrain data:

```bash
python scripts/update_terrain.py
```

Or load a small set of hardcoded sample roads:

```bash
python scripts/load_sample_roads.py
```

If you don't have any data, the API will still run but will return empty lists.

---

## 7. Run the Backend Server

Make sure you are in the `backend/` folder and the virtual environment is active.

Start the FastAPI server with:

```bash
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`.

---

## 8. Verify the API

Open your browser and go to:

- Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health/live`

You should see `{"status":"alive"}` for the health endpoint.

If you loaded road data, you can test `GET /api/v1/roads/` and `GET /api/v1/roads/risk`.

---

## 9. Troubleshooting

### Database connection error

- Make sure the Docker container is running (`docker ps`).
- Check that the `DATABASE_URL` in `.env` matches the credentials in `docker-compose.yml`.
- If you changed the password, update both files.

### PostGIS extension missing

- Run the `CREATE EXTENSION` commands again.
- If you get an error like `type "geometry" does not exist`, the extension is not enabled.

### `pip install` fails

- Ensure you have the correct Python version (3.10+).
- On Linux, you may need to install `python3-dev` and `build-essential`.
- For `psycopg2-binary`, no extra system packages are usually needed.

### Port conflicts

- If port 8000 is in use, run `uvicorn app.main:app --reload --port 8001`.
- If port 5432 is in use, change the port mapping in `docker-compose.yml` and update `DATABASE_URL`.

---

## Summary of Commands

```bash
# Clone and enter project
git clone https://github.com/SigmaSharmaG/Pravah.git
cd Pravah

# Copy environment file
cp .env.example .env

# Start database
docker-compose up -d db

# Enable PostGIS extensions (one-time)
docker exec -it <container_name> psql -U pravah -d pravah_db -c "CREATE EXTENSION IF NOT EXISTS postgis;"

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# (Optional) Load sample data
python scripts/load_geojson_roads.py data/roads.geojson

# Run server
uvicorn app.main:app --reload
```

Now you can access the API at `http://localhost:8000/docs`.

---

If you encounter any issues, please check the README or contact the team.
```