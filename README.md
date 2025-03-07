# CarePortal Backend

This is the backend of CarePortal.

## Tech Stack
- **Backend:** Python (FastAPI)
- **Database:** PostgreSQL
- **Deployment:** Docker containers

## Running the App Locally
Follow the steps below to run the application:

1. **Run the Database**
   - If using Docker, start a PostgreSQL container:
     ```sh
     docker run --name careportal-db -e POSTGRES_USER=<your_user> -e POSTGRES_PASSWORD=<your_password> -e POSTGRES_DB=careportal -p 5432:5432 -d postgres:latest
     ```
   - Alternatively, ensure PostgreSQL is running locally.

2. **Install Poetry** (if not already installed)
   ```sh
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install Dependencies**
   ```sh
   poetry install
   ```

4. **Run Database Migrations**
   ```sh
   poetry run alembic upgrade head
   ```

5. **Run the Application**
   ```sh
   poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

