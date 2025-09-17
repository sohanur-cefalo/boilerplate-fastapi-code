# 🍪 FastAPI Cookiecutter Template

A modern, production-ready **Cookiecutter template** for FastAPI projects with SQLAlchemy 2.0, PostgreSQL, and comprehensive configuration options.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed
- [Cookiecutter](https://cookiecutter.readthedocs.io/) installed

### Install Cookiecutter
```bash
pip install cookiecutter
```

### Generate Your Project

#### Option 1: From GitHub (Recommended)
```bash
# Replace with your actual GitHub repository URL
cookiecutter https://github.com/yourusername/fastapi-cookiecutter-template
```

#### Option 2: From Local Template
```bash
# If you have the template locally
cookiecutter /path/to/fastapi-cookiecutter-template
```

#### Option 3: Direct Clone & Generate
```bash
# Clone and generate in one go
git clone https://github.com/yourusername/fastapi-cookiecutter-template
cookiecutter fastapi-cookiecutter-template
```

### Interactive Setup
When you run the command, you'll be prompted with questions like:
```
project_name [My FastAPI Project]: My Awesome API
project_short_description [A FastAPI project with SQLAlchemy 2.0 and PostgreSQL]: My awesome API service
author_name [Your Name]: John Doe
author_email [your.email@example.com]: john@example.com
include_user_model [yes]: yes
include_authentication [basic]: jwt
development_environment [docker_db_local_app]: docker_db_local_app
include_testing [pytest]: pytest
include_github_actions [yes]: yes
```

### Non-Interactive Generation
```bash
# Generate with default values
cookiecutter https://github.com/yourusername/fastapi-cookiecutter-template --no-input

# Generate with custom values
cookiecutter https://github.com/yourusername/fastapi-cookiecutter-template --no-input \
  project_name="My Custom API" \
  include_user_model=yes \
  include_authentication=jwt \
  development_environment=full_docker
```

## ⚙️ Configuration Options

The template will prompt you for various options:

- **Project Details**: name, description, author
- **User Model**: Include complete user management (yes/no)
- **Authentication**: Basic, JWT, or none
- **Development Environment**: Docker+local, full Docker, or local
- **Features**: CORS, rate limiting, testing, GitHub Actions
- **Database**: PostgreSQL configuration

## 🏗️ Generated Features

### Core Stack
- ✅ **FastAPI** - Modern, fast web framework
- ✅ **SQLAlchemy 2.0** - Latest ORM with type annotations
- ✅ **PostgreSQL** - Production-ready database
- ✅ **Alembic** - Database migrations
- ✅ **Pydantic** - Data validation and settings

### Optional Features (Configurable)
- 👤 **User Management** - Complete CRUD with authentication
- 🔐 **JWT Authentication** - Secure token-based auth
- 🌐 **CORS & Rate Limiting** - Web security features
- 🧪 **Testing** - pytest with async support
- 🐳 **Docker** - Complete containerization
- 📊 **GitHub Actions** - CI/CD pipelines

## 🚦 Quick Examples

### Full-Featured Web App
```bash
cookiecutter path/to/template
# Choose: User model=yes, Auth=jwt, Environment=docker_db_local_app
```

### Minimal API Service
```bash
cookiecutter path/to/template
# Choose: User model=no, Auth=none, Environment=full_docker
```

## 🛠️ After Generation

Once your project is generated, follow these steps to get it running:

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

## 📝 Project Structure

```
your-project/
├── app/
│   ├── main.py              # FastAPI application
│   ├── core/config.py       # Settings
│   ├── api/v1/              # API routes
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── crud/                # Database operations
│   └── db/                  # Database session
├── alembic/                 # Migrations
├── tests/                   # Tests (optional)
├── docker-compose.yml       # Docker setup
├── requirements.txt
└── README.md               # Project-specific docs
```

## 🎯 Perfect For

- REST APIs with database
- Microservices
- Web applications with authentication
- Rapid prototyping
- Learning modern Python web development

## 🔧 Common Commands

### Project Generation Examples
```bash
# Minimal API (no user model, no auth)
cookiecutter https://github.com/yourusername/fastapi-cookiecutter-template --no-input \
  project_name="Simple API" \
  include_user_model=no \
  include_authentication=none \
  development_environment=full_docker

# Full-featured web app
cookiecutter https://github.com/yourusername/fastapi-cookiecutter-template --no-input \
  project_name="My Web App" \
  include_user_model=yes \
  include_authentication=jwt \
  development_environment=docker_db_local_app \
  include_testing=pytest \
  include_github_actions=yes

# Enterprise setup
cookiecutter https://github.com/yourusername/fastapi-cookiecutter-template --no-input \
  project_name="Enterprise API" \
  include_authentication=jwt \
  include_cors=yes \
  include_rate_limiting=yes \
  include_logging=structured
```

### Development Commands
```bash
# Database operations
alembic revision --autogenerate -m "Add new model"
alembic upgrade head
alembic downgrade -1

# Testing
pytest                          # Run all tests
pytest tests/test_users.py -v   # Run specific test file
pytest --cov=app               # Run with coverage

# Interactive shells
python management/shell.py              # Standard shell
python management/bpython_shell.py      # Enhanced shell (recommended)

# Docker operations
docker-compose up db -d         # Start database only
docker-compose up              # Start all services
docker-compose logs app        # View app logs
docker-compose down            # Stop all services
```

## 🚨 Troubleshooting

### Common Issues

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

### Getting Help
1. Check the generated project's `README.md` for project-specific instructions
2. Review the `.env` file for configuration options
3. Check `docker-compose logs` for container issues
4. Use the interactive shells to debug database issues

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

## 🤝 Contributing

Found a bug or want to add a feature to the template?

1. Fork this repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes to the template files
4. Test the template: `cookiecutter . --no-input`
5. Submit a pull request

---

**Happy coding! 🚀**
