# 🍪 FastAPI Cookiecutter Template

**A modern, production-ready Cookiecutter template for FastAPI projects with SQLAlchemy 2.0, PostgreSQL, and comprehensive configuration options.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green.svg)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)](https://sqlalchemy.org)
[![Cookiecutter](https://img.shields.io/badge/Cookiecutter-Template-yellow.svg)](https://github.com/cookiecutter/cookiecutter)

## 🚀 Quick Start

### 1. Install Cookiecutter
```bash
pip install cookiecutter
```

### 2. Generate Your Project
```bash
# Interactive setup (recommended for first-time users)
cookiecutter https://github.com/sohanur-cefalo/boilerplate-fastapi-code.git

# Quick generation with defaults
cookiecutter https://github.com/sohanur-cefalo/boilerplate-fastapi-code.git --no-input

# Custom configuration
cookiecutter https://github.com/sohanur-cefalo/boilerplate-fastapi-code.git --no-input \
  project_name="My Awesome API" \
  include_user_model=yes \
  include_authentication=jwt \
  development_environment=docker_db_local_app
```

### 3. Start Development
```bash
cd your-project-name
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# SQLite by default (no Docker needed)
alembic upgrade head || alembic revision --autogenerate -m "Initial" && alembic upgrade head
uvicorn app.main:app --reload
```

### 4. Access Your API
- **📚 API Docs**: http://localhost:8000/docs
- **🛠️ Admin Panel**: http://localhost:8000/admin
- **❤️ Health Check**: http://localhost:8000/health

## ⚡ What You Get

### 🏗️ **Flexible Architecture**
- **User Management**: Optional complete user CRUD with authentication
- **Authentication**: None, Basic, or JWT with login/logout
- **Development**: Docker+Local, Full Docker, or Local development
- **Testing**: pytest, unittest, or none
- **CI/CD**: GitHub Actions workflows

### 🔧 **Modern Tech Stack**
- **FastAPI** - High-performance async web framework
- **SQLAlchemy 2.0** - Modern ORM with type annotations
- **SQLite by default** - Simple local development, auto-created `app.db`
- **PostgreSQL option** - Swap by setting `DATABASE_URL` or using Docker
- **Alembic** - Database migrations
- **Pydantic** - Data validation and settings
- **Docker** - Containerization support
- **SQLAdmin** - Auto admin panel for all models at `/admin`

### 🎯 **Production Ready**
- Type-safe code throughout
- Comprehensive test suites
- Docker configurations
- Environment management
- Database migrations
- Interactive development shells
- CORS and rate limiting
- Structured logging options

## 📋 Template Options

| Option | Choices | Description |
|--------|---------|-------------|
| **User Model** | `yes` / `no` | Complete user management system |
| **Authentication** | `none` / `basic` / `jwt` | Authentication implementation |
| **Environment** | `docker_db_local_app` / `full_docker` / `local_development` | Development setup |
| **Testing** | `pytest` / `unittest` / `none` | Testing framework |
| **Docker** | `yes` / `no` | Docker configuration |
| **GitHub Actions** | `yes` / `no` | CI/CD pipeline |
| **CORS** | `yes` / `no` | Cross-origin support |
| **Rate Limiting** | `yes` / `no` | API rate limiting |

## 🎨 Project Examples

### Minimal API Service
```bash
cookiecutter https://github.com/sohanur-cefalo/boilerplate-fastapi-code.git --no-input \
  project_name="Simple API" \
  include_user_model=no \
  include_authentication=none \
  development_environment=full_docker \
  include_testing=none
```
**Result**: Clean API with Docker, no user management, no tests

### Full-Featured Web Application
```bash
cookiecutter https://github.com/sohanur-cefalo/boilerplate-fastapi-code.git --no-input \
  project_name="My Web App" \
  include_user_model=yes \
  include_authentication=jwt \
  development_environment=docker_db_local_app \
  include_testing=pytest \
  include_github_actions=yes
```
**Result**: Complete web app with user auth, JWT, tests, and CI/CD

### Enterprise API
```bash
cookiecutter https://github.com/sohanur-cefalo/boilerplate-fastapi-code.git --no-input \
  project_name="Enterprise API" \
  include_authentication=jwt \
  include_cors=yes \
  include_rate_limiting=yes \
  include_logging=structured \
  include_github_actions=yes
```
**Result**: Production-ready API with all enterprise features

## 📁 Generated Structure

```
your-project/
├── app/
│   ├── main.py              # FastAPI application
│   ├── core/config.py       # Configuration
│   ├── api/v1/              # API routes
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── crud/                # Database operations
│   └── db/                  # Database session
├── tests/                   # Test files (optional)
├── alembic/                 # Database migrations
├── management/              # Interactive shells
├── docker-compose.yml       # Docker setup
├── requirements.txt         # Dependencies
├── .env                     # Environment variables
└── README.md               # Project documentation
```

## 🚀 Development Workflows

### Docker DB + Local App (Recommended)
- Database runs in Docker (isolated, consistent)
- FastAPI runs locally (easy debugging, hot reload)
- Best of both worlds for development

### Full Docker
- Everything containerized
- Production-like environment
- Great for team consistency

### Local Development
- Everything runs on your machine
- Full control over environment
- Requires local PostgreSQL

## 🧪 Testing Your Template

```bash
# Test the template generation
python test_template.py

# Generate and test a sample project
cookiecutter . --no-input
cd my_fastapi_project
pip install -r requirements.txt
pytest
```

## 🛠️ After Generation - Complete Setup Guide

Once your project is generated, follow these steps:

### Step 1: Navigate to Your Project
```bash
cd your-project-name  # Replace with your actual project name
```

### Step 2: Choose Your Development Setup

#### 🐳 Option A: Docker DB + Local App (Recommended)
Perfect for development - database in Docker, app runs locally for easy debugging.

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start database only
docker-compose up db -d

# Wait for database to be ready (check with: docker-compose ps)
# Create database migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# Start the application
uvicorn app.main:app --reload
```

#### 🐳 Option B: Full Docker Setup
Everything runs in containers - good for production-like environment.

```bash
# Start everything with Docker
docker-compose up

# Or run in background
docker-compose up -d
```

#### 💻 Option C: Local Development
Everything runs locally - requires PostgreSQL installation.

```bash
# Install and start PostgreSQL locally
# Create database: createdb your_database_name

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment (edit .env file with your database settings)
# Create migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# Start the application
uvicorn app.main:app --reload
```

### Step 3: Access Your API
- **📚 API Documentation**: http://localhost:8000/docs
- **📖 Alternative Docs**: http://localhost:8000/redoc  
- **❤️ Health Check**: http://localhost:8000/health
- **🏠 Root Endpoint**: http://localhost:8000/

### Step 4: Verify Everything Works
```bash
# Test the API
curl http://localhost:8000/health

# Run tests (if included)
pytest

# Check database connection
python -c "from app.db.session import engine; print('✅ Database connected!')"
```

## 🔧 Common Commands & Troubleshooting

### Database Operations
```bash
# Create new migration
alembic revision --autogenerate -m "Add new model"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Check migration status
alembic current
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_users.py -v
```

### Docker Operations
```bash
# Start database only
docker-compose up db -d

# Start all services
docker-compose up

# View logs
docker-compose logs app
docker-compose logs db

# Stop services
docker-compose down
```

### Common Issues & Solutions

#### "ModuleNotFoundError" when running the app
```bash
# Make sure you're in the virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

#### Database connection errors
```bash
# Check if database is running
docker-compose ps

# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

#### Port already in use
```bash
# Find what's using the port
lsof -i :8000

# Or change the port in your .env file
API_PORT=8001
```

#### Alembic migration issues
```bash
# Reset migrations (careful - this deletes data!)
rm alembic/versions/*.py
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## 🤝 Contributing

1. Fork this repository
2. Make your changes
3. Test with: `cookiecutter . --no-input`
4. Submit a pull request

## 📄 License

This template is licensed under the MIT License. Generated projects can use any license you choose.

---

**🎉 Ready to build amazing FastAPI applications? Get started now!**

```bash
pip install cookiecutter
cookiecutter https://github.com/sohanur-cefalo/boilerplate-fastapi-code.git
```

**⭐ Star this repo if it helps you build better APIs faster!**