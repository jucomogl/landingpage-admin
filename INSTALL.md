# CMS Installation Guide (Dockerized)

## Requirements:
- Docker
- Docker Compose

## Installation Steps:
1. Clone or download the CMS files.
2. Open a terminal and navigate to the project directory.
3. Build and run the Docker container:
   ```sh
   docker-compose up --build
   ```
4. Open your web browser and go to:
   ```
   http://127.0.0.1:5000
   ```
5. A login screen will appear. Default credentials:
   - Username: `admin`
   - Password: `admin123`
6. After login, you can add sections, edit the footer, and update the logo.

## Resetting Password:
- Click **Forgot Password?** and enter your email.
- An email with a reset link will be sent.

## Database:
- The CMS uses `cms.db` (SQLite) for storing data.
- To access the database inside the container:
   ```sh
   docker exec -it <container_id> sqlite3 /app/cms.db
   ```