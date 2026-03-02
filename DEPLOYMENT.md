## Deployment & CI/CD (Overview)

I would package the solution as a Docker image and deploy it either with **Docker Compose (single server)** or **Kubernetes / a cloud platform** depending on the environment.

In a simple production setup, I’d use **Docker Compose** to run:

* the **FastAPI** container
* the **PostgreSQL** container (with a persistent volume)

Configuration is handled via **environment variables** (DB credentials, debug flags, API host, etc.). After starting the containers, the deployment runs **database migrations** and optionally imports the initial CSV data. In front of the API I’d place a **reverse proxy** (e.g., Nginx/Traefik) to enable **HTTPS** and handle routing. The service exposes `/api/health` for readiness/liveness checks, and logs are collected from the containers.

For a more scalable setup, I’d deploy the same Docker image to **Kubernetes** (or a managed cloud equivalent). In that case:

* the API runs as a **Deployment** with multiple replicas
* configuration comes from **ConfigMaps/Secrets**
* the service is exposed through an **Ingress / Load Balancer**
* PostgreSQL is preferably **managed** (RDS/Azure Database/Cloud SQL), while health probes rely on the same `/api/health` endpoint.

For CI/CD (GitHub Actions / GitLab CI), the pipeline would typically include:

* **Test**: build the image, run unit tests, lint/static checks
* **Security / Vulnerability Scan**: scan the image and Python dependencies for known vulnerabilities
* **Build & Push**: build a production image, tag it (commit SHA + latest), push to a container registry
* **Deploy**: update the running environment

  * Compose: pull the new image and restart containers
  * Kubernetes/cloud: update the deployment image, run migrations as a job (or controlled step), and roll out the new version

The pipeline runs on pull requests (tests only) and on merges to `main` (build + deploy).
