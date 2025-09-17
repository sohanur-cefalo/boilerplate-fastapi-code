# {{cookiecutter.project_name}}

{{cookiecutter.project_short_description}}

Generated with [FastAPI Cookiecutter Template](https://github.com/sohanur-cefalo/boilerplate-fastapi-code).

## 🚀 Quick Start

{% if cookiecutter.development_environment == "docker_db_local_app" -%}
### Docker DB + Local App Setup (Recommended)

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start database
docker-compose up db -d

# 4. Run migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# 5. Start the application
uvicorn app.main:app --reload
```

{% elif cookiecutter.development_environment == "full_docker" -%}
### Full Docker Setup

```bash
# Start everything with Docker
docker-compose up

# Or run in background
docker-compose up -d
```

{% else -%}
### Local Development Setup

```bash
# 1. Create PostgreSQL database
createdb {{cookiecutter.database_name}}

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
# Edit .env with your database settings

# 5. Run migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# 6. Start the application
uvicorn app.main:app --reload
```
{% endif -%}

## 🌐 Access Your API

- **API Documentation**: http://localhost:{{cookiecutter.api_port}}/docs
- **Alternative Docs**: http://localhost:{{cookiecutter.api_port}}/redoc
- **Health Check**: http://localhost:{{cookiecutter.api_port}}/health

{% if cookiecutter.include_user_model == "yes" -%}
## 👤 User API Endpoints

- `GET /api/v1/users/` - List all users
- `GET /api/v1/users/{user_id}` - Get user by ID
- `POST /api/v1/users/` - Create new user
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

{% if cookiecutter.include_authentication == "jwt" -%}
### Authentication Endpoints

- `POST /api/v1/users/token` - Login and get access token
- `GET /api/v1/users/me` - Get current user profile

### Example Usage

```bash
# Create a user
curl -X POST "http://localhost:{{cookiecutter.api_port}}/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "username": "johndoe",
    "password": "secretpassword"
  }'

# Login to get token
curl -X POST "http://localhost:{{cookiecutter.api_port}}/api/v1/users/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=secretpassword"

# Use token to access protected endpoints
curl -X GET "http://localhost:{{cookiecutter.api_port}}/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
{% endif -%}
{% endif -%}

## 🏗️ Project Structure

```
{{cookiecutter.project_slug}}/
├── app/
│   ├── main.py              # FastAPI application
│   ├── core/
│   │   └── config.py        # Configuration settings
│   ├── api/
│   │   └── v1/
│   │       ├── api.py       # API router
│   │       └── endpoints/   # API endpoints
│   ├── crud/                # Database operations
│   ├── db/
│   │   └── session.py       # Database session
│   ├── models/              # SQLAlchemy models
│   └── schemas/             # Pydantic schemas
├── alembic/                 # Database migrations
├── management/              # Interactive shells
{% if cookiecutter.include_testing != "none" -%}
├── tests/                   # Test files
{% endif -%}
{% if cookiecutter.include_docker == "yes" -%}
├── Dockerfile
├── docker-compose.yml
{% endif -%}
├── requirements.txt
├── .env                     # Environment variables
└── README.md
```

## 🗄️ Database Operations

### Create Migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Interactive Shell
```bash
# Standard Python shell with database access
python management/shell.py

# Enhanced shells (if installed)
python management/bpython_shell.py  # Recommended
python management/ipython_shell.py
```

{% if cookiecutter.include_testing != "none" -%}
## 🧪 Testing

{% if cookiecutter.include_testing == "pytest" -%}
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_users.py -v
```
{% else -%}
```bash
# Run all tests
python -m unittest discover tests

# Run specific test
python -m unittest tests.test_users
```
{% endif -%}
{% endif -%}

## 📝 Adding New Models

1. **Create Model**: `app/models/your_model.py`
2. **Create Schema**: `app/schemas/your_model.py`
3. **Create CRUD**: `app/crud/your_model.py`
4. **Create Endpoints**: `app/api/v1/endpoints/your_model.py`
5. **Update Router**: Add to `app/api/v1/api.py`
6. **Create Migration**: `alembic revision --autogenerate -m "Add your model"`

{% if cookiecutter.include_docker == "yes" -%}
## 🐳 Docker Commands

```bash
# Build image
docker build -t {{cookiecutter.project_slug}} .

# Run container
docker run -p {{cookiecutter.api_port}}:{{cookiecutter.api_port}} {{cookiecutter.project_slug}}

# Docker Compose
docker-compose up -d          # Start in background
docker-compose logs app       # View app logs
docker-compose logs db        # View database logs
docker-compose down           # Stop all services
```
{% endif -%}

## ⚙️ Configuration

Environment variables are configured in `.env`:

```env
# Database
DATABASE_URL=postgresql://{{cookiecutter.database_user}}:{{cookiecutter.database_password}}@{{cookiecutter.database_host}}:{{cookiecutter.database_port}}/{{cookiecutter.database_name}}

# Application
DEBUG={% if cookiecutter.development_environment != "full_docker" %}True{% else %}False{% endif %}
PROJECT_NAME={{cookiecutter.project_name}}
VERSION={{cookiecutter.version}}

{% if cookiecutter.include_authentication != "none" -%}
# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
{% endif -%}
```

## 🚀 Deployment

{% if cookiecutter.include_docker == "yes" -%}
### Docker Production
```bash
docker build -t {{cookiecutter.project_slug}}:latest .
docker run -p {{cookiecutter.api_port}}:{{cookiecutter.api_port}} \
  -e DATABASE_URL="your-production-db-url" \
  {% if cookiecutter.include_authentication != "none" -%}-e SECRET_KEY="your-production-secret" \{% endif %}
  {{cookiecutter.project_slug}}:latest
```
{% endif -%}

### Environment Variables for Production
- Set `DEBUG=False`
- Use a strong `SECRET_KEY`
- Configure production database URL
- Set appropriate CORS origins

## 📚 Tech Stack

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy 2.0** - ORM with type annotations
- **PostgreSQL** - Production database
- **Alembic** - Database migrations
- **Pydantic** - Data validation
{% if cookiecutter.include_authentication == "jwt" -%}
- **JWT** - Token-based authentication
{% endif -%}
{% if cookiecutter.include_testing == "pytest" -%}
- **pytest** - Testing framework
{% endif -%}
{% if cookiecutter.include_docker == "yes" -%}
- **Docker** - Containerization
{% endif -%}

## 📄 License

This project is licensed under the {{cookiecutter.license}} License.

---

**Author**: {{cookiecutter.author_name}} ({{cookiecutter.author_email}})  
**Version**: {{cookiecutter.version}}
