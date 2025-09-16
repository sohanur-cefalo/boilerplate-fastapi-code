#!/usr/bin/env python3
"""
FastAPI Boilerplate Project Starter
===================================

This script helps you quickly set up a new FastAPI project from this boilerplate.

Usage:
    python start_project.py my_new_project

Features:
- Copies boilerplate code to new project directory
- Updates project name in configuration
- Sets up initial git repository
- Provides next steps instructions
"""

import os
import sys
import shutil
import subprocess
import re
from pathlib import Path

def get_user_input(prompt, default_value):
    """Get user input with robust handling"""
    import sys
    
    try:
        # Try standard input first
        user_input = input(prompt)
    except:
        # Fallback for problematic terminals
        print(prompt, end="", flush=True)
        user_input = sys.stdin.readline().strip()
    
    # Clean input - remove all non-alphanumeric characters except hyphens and underscores
    user_input = re.sub(r'[^\w\-_]', '', user_input)
    
    # Use default if empty after cleaning
    if not user_input:
        return default_value
    else:
        return user_input

def main():
    # Interactive project name input
    if len(sys.argv) == 2:
        # If project name provided as argument, use it
        project_name = sys.argv[1]
    else:
        # Interactive mode - ask for project name
        print("🚀 FastAPI Project Generator")
        print("=" * 40)
        print("Create a new FastAPI project with SQLAlchemy 2.0")
        print()
        
        # Get project name with default
        default_name = "my-fastapi-project"
        
        try:
            # Get project name with robust input handling
            project_name = get_user_input(f"📝 Project name [{default_name}]: ", default_name)
            
            if project_name == default_name:
                print(f"✅ Using default name: {project_name}")
            else:
                print(f"✅ Using name: {project_name}")
                
        except (EOFError, KeyboardInterrupt):
            # Handle Ctrl+C or EOF
            print(f"\n✅ Using default name: {default_name}")
            project_name = default_name
        
        # Validate project name
        if not project_name.replace('-', '').replace('_', '').isalnum():
            print("❌ Project name can only contain letters, numbers, hyphens, and underscores")
            sys.exit(1)
    
        print()
    current_dir = Path(__file__).parent
    project_dir = current_dir.parent / project_name
    
    print(f"🚀 Creating new FastAPI project: {project_name}")
    print(f"📁 Project directory: {project_dir}")
    
    # Check if directory already exists
    if project_dir.exists():
        print(f"❌ Directory {project_dir} already exists!")
        print("Please choose a different project name or remove the existing directory.")
        sys.exit(1)
    
    try:
        # Copy boilerplate code
        print("📋 Copying boilerplate code...")
        shutil.copytree(current_dir, project_dir, ignore=shutil.ignore_patterns(
            '__pycache__', '*.pyc', '.git', '.DS_Store', 'alembic/versions/*.py', 'templates'
        ))
        
        # Ensure alembic/versions directory exists
        versions_dir = project_dir / "alembic" / "versions"
        versions_dir.mkdir(parents=True, exist_ok=True)
        
        # Update project name in config
        print("⚙️  Updating project configuration...")
        config_file = project_dir / "app" / "core" / "config.py"
        if config_file.exists():
            content = config_file.read_text()
            content = content.replace(
                'project_name: str = "Your FastAPI Project"',
                f'project_name: str = "{project_name.replace("_", " ").title()}"'
            )
            config_file.write_text(content)
        
        # Update alembic env.py to import all models for auto-detection
        print("🔧 Updating Alembic configuration for auto-detection...")
        alembic_env_file = project_dir / "alembic" / "env.py"
        if alembic_env_file.exists():
            content = alembic_env_file.read_text()
            
            # Check if models are already imported
            if "from app.models import" not in content:
                # Find the line with Base import and add model imports after it
                lines = content.split('\n')
                new_lines = []
                for line in lines:
                    new_lines.append(line)
                    if "from app.db.session import Base" in line:
                        new_lines.append("")
                        new_lines.append("# Import all models to make them discoverable for Alembic")
                        new_lines.append("from app.models import *  # This will import all models automatically")
                        new_lines.append("")
                
                # Write the updated content
                alembic_env_file.write_text('\n'.join(new_lines))
        
        # Create database readiness check script
        print("📝 Creating database readiness check script...")
        db_check_script = project_dir / "check_db.py"
        db_check_content = '''#!/usr/bin/env python3
"""
Database Readiness Check Script
Run this to verify your database connection is working.
"""
import sys
import time
from sqlalchemy import create_engine, text
from app.core.config import settings

def check_database_connection():
    """Check if database is ready and accessible"""
    print("🔍 Checking database connection...")
    print(f"Database URL: {settings.database_url}")
    
    max_retries = 10
    retry_delay = 3
    
    for attempt in range(max_retries):
        try:
            engine = create_engine(settings.database_url)
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print("✅ Database connection successful!")
                return True
        except Exception as e:
            print(f"❌ Attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                print(f"⏳ Waiting {retry_delay} seconds before retry...")
                time.sleep(retry_delay)
            else:
                print("❌ All connection attempts failed!")
                print("💡 Make sure your database is running:")
                print("   docker-compose ps")
                print("   docker-compose logs db")
                return False
    
    return False

if __name__ == "__main__":
    success = check_database_connection()
    sys.exit(0 if success else 1)
'''
        db_check_script.write_text(db_check_content)
        db_check_script.chmod(0o755)
        
        # Ask user about user table
        print("👤 Do you want to include a User table?")
        print("1. Yes, include User table (default)")
        print("2. No, create minimal project without User table")
        print()
        
        try:
            user_choice = input("Enter choice (1/2) [1]: ").strip()
            if not user_choice:
                user_choice = "1"
        except (EOFError, KeyboardInterrupt):
            print("\n✅ Using default choice: 1")
            user_choice = "1"
        
        # Remove user table if not needed
        if user_choice == "2":
            print("🗑️  Removing User table and related files...")
            # Remove user model
            user_model_file = project_dir / "app" / "models" / "user.py"
            if user_model_file.exists():
                user_model_file.unlink()
            
            # Remove user schema
            user_schema_file = project_dir / "app" / "schemas" / "user.py"
            if user_schema_file.exists():
                user_schema_file.unlink()
            
            # Remove user CRUD
            user_crud_file = project_dir / "app" / "crud" / "user.py"
            if user_crud_file.exists():
                user_crud_file.unlink()
            
            # Remove user endpoints
            user_endpoints_file = project_dir / "app" / "api" / "v1" / "endpoints" / "users.py"
            if user_endpoints_file.exists():
                user_endpoints_file.unlink()
            
            # Update models __init__.py
            models_init_file = project_dir / "app" / "models" / "__init__.py"
            if models_init_file.exists():
                models_init_file.write_text("# Import all models here to make them discoverable for Alembic\n# Add your models below\n\n# Export all models\n__all__ = []\n")
            
            # Update schemas __init__.py
            schemas_init_file = project_dir / "app" / "schemas" / "__init__.py"
            if schemas_init_file.exists():
                schemas_init_file.write_text("# Import all schemas here\n# Add your schemas below\n\n# Export all schemas\n__all__ = []\n")
            
            # Update CRUD __init__.py
            crud_init_file = project_dir / "app" / "crud" / "__init__.py"
            if crud_init_file.exists():
                crud_init_file.write_text("# Import all CRUD operations here\n# Add your CRUD operations below\n\n# Export all CRUD operations\n__all__ = []\n")
            
            # Update API router
            api_router_file = project_dir / "app" / "api" / "v1" / "api.py"
            if api_router_file.exists():
                api_router_file.write_text("from fastapi import APIRouter\n\n# Import your routers here\n# from app.api.v1.endpoints import your_router\n\napi_router = APIRouter()\n\n# Add your routers here\n# api_router.include_router(your_router.router, prefix=\"/your-endpoint\", tags=[\"your-tag\"])\n")
        
        # Update alembic env.py to import all models for auto-detection
        print("🔧 Updating Alembic configuration for auto-detection...")
        alembic_env_file = project_dir / "alembic" / "env.py"
        if alembic_env_file.exists():
            content = alembic_env_file.read_text()
            
            # Check if models are already imported
            if "from app.models import" not in content:
                # Find the line with Base import and add model imports after it
                lines = content.split('\n')
                new_lines = []
                for line in lines:
                    new_lines.append(line)
                    if "from app.db.session import Base" in line:
                        new_lines.append("")
                        new_lines.append("# Import all models to make them discoverable for Alembic")
                        new_lines.append("from app.models import *  # This will import all models automatically")
                        new_lines.append("")
                
                # Write the updated content
                alembic_env_file.write_text('\n'.join(new_lines))
        
        # Ask user for development method
        print("📋 Choose your development method:")
        print("1. Full Docker (app + database)")
        print("2. Docker DB + Local App (recommended)")
        print("3. Local development (requires PostgreSQL)")
        print()
        
        try:
            choice = input("Enter choice (1/2/3) [2]: ").strip()
            if not choice:
                choice = "2"
        except (EOFError, KeyboardInterrupt):
            print("\n✅ Using default choice: 2")
            choice = "2"
        
        # Create project README based on choice
        print("📝 Creating project README...")
        readme_file = project_dir / "README.md"
        project_title = project_name.replace('_', ' ').title()
        
        # Load appropriate templates
        template_dir = current_dir / "templates"
        if choice == "1":
            readme_template = template_dir / "README_full_docker.md"
            docker_compose_template = template_dir / "docker-compose_full.yml"
            env_template = template_dir / "env_full_docker.example"
        elif choice == "3":
            readme_template = template_dir / "README_local_development.md"
            docker_compose_template = None  # No docker-compose for local development
            env_template = template_dir / "env_local_development.example"
        else:  # choice == "2" or default
            readme_template = template_dir / "README_docker_db_local_app.md"
            docker_compose_template = template_dir / "docker-compose_db_only.yml"
            env_template = template_dir / "env_docker_db_local_app.example"
        
        # Read and format README template
        with open(readme_template, 'r') as f:
            readme_content = f.read()
        
        # Replace placeholders
        readme_content = readme_content.replace("{project_title}", project_title)
        readme_content = readme_content.replace("{project_name}", project_name)
        readme_content = readme_content.replace("{project_name.lower()}", project_name.lower())
        
        # Write README
        readme_file.write_text(readme_content)
        
        # Update docker-compose.yml based on choice
        if docker_compose_template:
            print("🐳 Updating docker-compose configuration...")
            with open(docker_compose_template, 'r') as f:
                docker_compose_content = f.read()
            
            docker_compose_file = project_dir / "docker-compose.yml"
            docker_compose_file.write_text(docker_compose_content)
        
        # Update .env.example based on choice
        print("⚙️  Updating environment configuration...")
        with open(env_template, 'r') as f:
            env_content = f.read()
        
        # Replace placeholders in env file
        env_content = env_content.replace("{project_title}", project_title)
        env_content = env_content.replace("{project_name}", project_name)
        env_content = env_content.replace("{project_name.lower()}", project_name.lower())
        
        env_file = project_dir / "env.example"
        env_file.write_text(env_content)
        
        # Initialize git repository
        print("🔧 Initializing git repository...")
        try:
            subprocess.run(["git", "init"], cwd=project_dir, check=True)
            subprocess.run(["git", "branch", "-m", "main"], cwd=project_dir, check=True)
            subprocess.run(["git", "add", "."], cwd=project_dir, check=True)
            subprocess.run(["git", "commit", "-m", f"Initial commit for {project_title}"], cwd=project_dir, check=True)
            print("✅ Git repository initialized with 'main' branch")
        except subprocess.CalledProcessError:
            print("⚠️  Git initialization failed (git might not be installed)")
        
        print()
        print("=" * 60)
        print("🎉 Project created successfully!")
        print("=" * 60)
        print()
        print(f"📁 Project location: {project_dir}")
        print()
        print(f"📝 Project README: {project_dir}/README.md")
        print()
        
        # Show next steps based on choice
        print("=" * 40)
        print("🚀 Next Steps")
        print("=" * 40)
        print()
        
        if choice == "1":
            print("🐳 Full Docker development setup:")
            print(f"1. cd {project_dir}")
            print("2. docker-compose up")
            print("\n🌐 Visit http://localhost:8000/docs for API documentation")
            print("📊 Database will be automatically set up!")
        elif choice == "3":
            print("🔧 Local development setup:")
            print(f"1. cd {project_dir}")
            print("2. Install PostgreSQL locally")
            print("3. Create database: createdb {project_name.lower()}")
            print("4. cp env.example .env")
            print("5. Edit .env with your database settings")
            print("6. pip install -r requirements.txt")
            print("7. alembic revision --autogenerate -m 'Initial migration'")
            print("8. alembic upgrade head")
            print("9. uvicorn app.main:app --reload")
            print("\n🌐 Visit http://localhost:8000/docs for API documentation")
        else:  # choice == "2"
            print("🐳 Docker DB + Local App setup:")
            print(f"1. cd {project_dir}")
            print("2. python -m venv env")
            print("3. Activate virtual environment:")
            print("   - Windows: env\\Scripts\\activate")
            print("   - macOS/Linux: source env/bin/activate")
            print("4. pip install -r requirements.txt")
            print("5. docker-compose up db -d")
            print("6. Wait for database to be ready (check with: docker-compose ps)")
            print("7. cp env.example .env")
            print("8. python check_db.py  # Verify database connection")
            print("9. alembic revision --autogenerate -m 'Initial migration'")
            print("10. alembic upgrade head")
            print("11. uvicorn app.main:app --reload")
            print("\n🌐 Visit http://localhost:8000/docs for API documentation")
            print("📊 Database runs on port 54321 (no conflicts!)")
            print("\n💡 If you get connection errors, run: python check_db.py")
            print("💡 Database needs time to fully initialize after docker-compose up.")
        
        print()
        print("📚 Read the project README.md for complete instructions")
        print("=" * 60)
        
        # Output the project directory path for shell navigation
        print(f"\n📁 Project created in: {project_dir}")
        print(f"💡 To navigate to your project, run: cd {project_dir}")
        print(f"💡 Or use: cd {project_name}")
        
        # Output project name for shell capture (prefixed with special marker)
        print(f"PROJECT_NAME_OUTPUT:{project_name}")
        
    except Exception as e:
        print(f"❌ Error creating project: {e}")
        if project_dir.exists():
            print(f"🧹 Cleaning up project directory: {project_dir}")
            shutil.rmtree(project_dir)
        print("💡 The temp-boilerplate directory will be cleaned up automatically")
        sys.exit(1)

if __name__ == "__main__":
    main()
