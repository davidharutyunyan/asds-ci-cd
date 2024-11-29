# Summary of Tasks

## Task 1: Fix the Shared Volumes Issue
**Objective:** Ensure two services (`writer` and `reader`) share a volume to collaborate effectively.  

### Steps:
1. Define a shared volume (`shared-data`) in the `docker-compose.yml` file.
2. Mount the `shared-data` volume for both services to allow shared access to files.
3. Ensure persistence by configuring the volume as a named volume in `docker-compose.yml`.

---

## Task 2: Implement Scheduled Tasks Using Docker Compose with Restarts
**Objective:** Update the `writer` service to run periodically using Docker Compose's `restart` policy.  

### Steps:
1. Update the `docker-compose.yml` file to:
   - Set `restart: always` for the `writer` service.
   - Add a `deploy.restart_policy` configuration with a delay (e.g., `delay: 60s`) to schedule periodic execution.
2. Modify the `writer.py` script to run once and exit after completing its task (remove any infinite loops).
3. Test the setup to ensure the `writer` service runs periodically and works with the `reader` service.

---