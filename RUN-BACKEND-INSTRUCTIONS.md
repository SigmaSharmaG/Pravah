```markdown
# How to Run Pravah Backend

This guide explains how to set up and run the Pravah Logistics Intelligence backend on your local machine. The backend is built with FastAPI, PostgreSQL/PostGIS, and can be run either using Docker Compose (recommended) or directly with Python.

---

## Prerequisites

- **Git** – [Download](https://git-scm.com/)
- **Docker** – [Download](https://docs.docker.com/get-docker/)
- **Docker Compose** – included with Docker Desktop, or install separately on Linux
- **Python 3.10+** (if running locally) – [Download](https://www.python.org/downloads/)
- **pip** (if running locally)

---

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/Pravah.git
cd Pravah
```

---

## 2. Environment Configuration

Create a `.env` file in the project root (where `docker-compose.yml` is located). You can copy the example:

```bash
cp .env.example .env
```

Edit `.env` and set at least these variables:

```env
SECRET_KEY=change-this-to-a-random-secret
DATABASE_URL=postgresql://pravah:pravah123@localhost:5433/pravah_db
```

If you are running locally without Docker, use port `5432` instead (see section 5).

---

## 3. Running with Docker Compose (Recommended)

This starts both the PostgreSQL/PostGIS database and the FastAPI backend in containers.

```bash
docker-compose up --build
```

The first build may take a few minutes.

- Backend API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- Database: accessible on host port `5433` (if you need to connect from host tools)

**Note:** The database port is mapped to `5433` on the host to avoid conflicts with any local PostgreSQL on `5432`.

To run in detached mode (background):

```bash
docker-compose up -d --build
```

To stop:

```bash
docker-compose down
```

---

## 4. Loading Road Data

The database starts empty. You need to load road segments before the system can route.

### Option A: Load Sample Data (Quick)

This creates a small, fully connected network for testing (nodes 1001–1005).

```bash
cd backend
python scripts/load_sample_roads.py
```

### Option B: Load Real Data from GeoJSON

If you have a GeoJSON file of road lines (e.g., downloaded from Overpass Turbo), place it in `backend/data/roads.geojson`, then run:

```bash
cd backend
python scripts/load_geojson_roads.py data/roads.geojson
```

### Option C: Prune to Largest Connected Component

If your real data has multiple disconnected parts, use:

```bash
python scripts/prune_to_largest_component.py
```

**Important:** Run these scripts from the `backend/` directory, and make sure the `DATABASE_URL` in `.env` points to the correct host port (e.g., `localhost:5433` if using Docker, or `localhost:5432` if running locally). If you get a connection error, check the section "Troubleshooting".

---

## 5. Running Locally Without Docker

If you prefer to run the backend directly on your machine (e.g., for development), follow these steps:

### 5.1 Start PostgreSQL/PostGIS

You can still use Docker only for the database:

```bash
docker-compose up -d db
```

This will start the database on port `5433`. Then set `DATABASE_URL` accordingly.

### 5.2 Install Python Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 5.3 Run the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

---

## 6. Authentication

The API is protected with JWT authentication. To use the system:

1. Register a new user via `POST /api/v1/auth/register` in Swagger UI or using any HTTP client.
2. Login via `POST /api/v1/auth/login` (form data: `username`, `password`).
3. Copy the `access_token` from the response.
4. In Swagger UI, click the **Authorize** button and paste the token.

For automated demos, a default user can be seeded:

```bash
python scripts/seed_user.py
```

This creates `demo / demo123`.

---

## 7. Testing the Workflow

1. **Login** to get a token.
2. **Create a shipment** (`POST /api/v1/shipments/`) with place names or node IDs.
3. **Get route recommendation** (`POST /api/v1/routes/recommend?shipment_id=<id>`).
4. **Add an incident** on one of the route segments (`POST /api/v1/incidents/`).
5. **Wait for alert** (background monitor runs every 30 seconds; or manually call the check).
6. **Reroute** (`POST /api/v1/shipments/<id>/reroute`) – the system will either suggest an alternative or refuse if no safe path exists.

---

## 8. Troubleshooting

### Database Connection Error

- If using Docker, ensure the database container is healthy: `docker ps`.
- Check that `DATABASE_URL` matches the host port: `5433` for Docker, `5432` for local.
- If you changed the database password after the volume was created, Docker ignores the new password because the volume persists old data. Delete the volume and restart:
  ```bash
  docker-compose down
  docker volume rm pravah_postgres_data   # adjust volume name if needed
  docker-compose up -d
  ```

### PostGIS Extension Missing

If you get `type "geometry" does not exist`, the PostGIS extension wasn't created. The Docker setup uses an init script (`infrastructure/docker/init.sql`) to create it automatically on first run. If you're not using Docker, run manually:
```sql
CREATE EXTENSION IF NOT EXISTS postgis;
```

### Port Conflicts

- If port `5433` or `8000` is already in use, change the mapping in `docker-compose.yml` or run the server on a different port.
- For local development, you can use `uvicorn app.main:app --reload --port 8001`.

### Authentication Errors

- Ensure you include the token in the `Authorization` header as `Bearer <token>`.
- If the token expired, login again.

---

## Summary

```bash
# With Docker (recommended)
git clone <repo>
cd Pravah
cp .env.example .env   # edit SECRET_KEY if needed
docker-compose up --build
cd backend
python scripts/load_sample_roads.py   # or other loading script
# Access http://localhost:8000/docs
```

---

For any issues, please check the project README or contact the team.
```