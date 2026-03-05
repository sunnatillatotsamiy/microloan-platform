# MicroLoan Platform

A full-stack micro-lending web application built with Django, Docker, and deployed to Azure with a complete CI/CD pipeline.

**Live URL:** https://dscc-15751-wiut.duckdns.org

---

## Features

- User registration, login, and logout
- Two user roles: Customer and Manager
- Loan application form with dynamic interest rate calculator
- Manager dashboard to approve or reject loan applications
- User management (CRUD) for managers
- Real-time loan summary with monthly payment calculation
- Admin panel for database management
- REST API with JWT authentication

---

## Technologies

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2, Django REST Framework |
| Database | PostgreSQL 15 |
| Web Server | Nginx + Gunicorn |
| Containerisation | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Cloud | Microsoft Azure VM (Ubuntu 24.04) |
| SSL | Let's Encrypt (Certbot) |
| Image Registry | Docker Hub |

---

## Database Models

- **User** — extends AbstractUser with `role` (customer/manager/admin) and `phone_number` fields
- **LoanProduct** — loan types with interest rates and amount/duration ranges
- **LoanApplication** — customer loan requests with status tracking (ManyToOne: User, LoanProduct)
- **RiskTag** — tags for loan risk classification (ManyToMany with LoanApplication)
- **ManagerReview** — manager decisions with comments (ManyToOne: LoanApplication)

---

## Local Setup

### Prerequisites
- Docker and Docker Compose installed
- Git

### Steps
```bash
# Clone the repository
git clone https://github.com/sunnatillatotsamiy/microloan-platform.git
cd microloan-platform

# Create .env file
cp .env.example .env
# Edit .env with your values

# Build and start
docker compose up -d --build

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# Visit http://localhost:8000
```

---

## Environment Variables

Create a `.env` file in the project root (see `.env.example`):
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

POSTGRES_DB=microloan_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-db-password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

---

## Deployment

### Server Requirements
- Ubuntu 24.04 LTS
- Docker and Docker Compose installed
- Ports 22, 80, 443 open in firewall

### Steps
```bash
# SSH into server
ssh user@your-server-ip

# Clone repository
git clone https://github.com/sunnatillatotsamiy/microloan-platform.git
cd microloan-platform

# Create .env with production values
nano .env

# Start services
docker compose up -d --build

# Run migrations
docker compose exec web python manage.py migrate

# Collect static files
docker compose exec web python manage.py collectstatic --noinput
```

### SSL Setup
```bash
sudo apt install certbot
docker compose stop nginx
sudo certbot certonly --standalone -d yourdomain.com
docker compose up -d
```

---

## CI/CD Pipeline

Pushes to `main` automatically trigger:

1. **Test** — flake8 linting + 10 Django unit tests
2. **Build** — Docker image built and pushed to Docker Hub
3. **Deploy** — SSH into Azure VM, pull image, restart containers, run migrations

### GitHub Secrets Required

| Secret | Description |
|--------|-------------|
| DOCKERHUB_USERNAME | Docker Hub username |
| DOCKERHUB_TOKEN | Docker Hub access token |
| SSH_HOST | Azure VM public IP |
| SSH_USERNAME | SSH username |
| SSH_PASSWORD | SSH password |

---

## Test Credentials

| Role | Username | Password |
|------|----------|----------|
| Customer | testuser | Test1234! |
| Manager | manager1 | Manager123! |

---

## Project Structure
```
microloan-platform/
├── .github/workflows/ci.yml   # CI/CD pipeline
├── config/                    # Django settings and URLs
├── loans/                     # Loan models, views, API
├── users/                     # User models, views, API
├── templates/                 # HTML templates
├── nginx/                     # Nginx configuration
├── Dockerfile                 # Multi-stage production build
├── docker-compose.yml         # Multi-container setup
├── requirements.txt
└── .env.example
```
