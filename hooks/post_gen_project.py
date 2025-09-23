#!/usr/bin/env python3
"""
Post-generation hook for FastAPI Cookiecutter template.
This script runs after the project is generated and handles:
- Conditional file cleanup based on user choices
- Setting up the development environment
- Creating initial git repository
"""

import os
import shutil
import subprocess
from pathlib import Path

def remove_file_if_exists(filepath):
    """Remove a file if it exists"""
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"Removed: {filepath}")

def remove_dir_if_exists(dirpath):
    """Remove a directory if it exists"""
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)
        print(f"Removed directory: {dirpath}")

def main():
    """Main post-generation processing"""
    
    # Get template variables
    include_user_model = "{{ cookiecutter.include_user_model }}"
    include_docker = "{{ cookiecutter.include_docker }}"
    include_testing = "{{ cookiecutter.include_testing }}"
    include_github_actions = "{{ cookiecutter.include_github_actions }}"
    development_environment = "{{ cookiecutter.development_environment }}"
    
    print("🔧 Running post-generation setup...")
    
    # Remove user model files if not needed
    if include_user_model == "no":
        print("🗑️  Removing user model files...")
        remove_file_if_exists("app/models/user.py")
        remove_file_if_exists("app/schemas/user.py") 
        remove_file_if_exists("app/crud/user.py")
        remove_file_if_exists("app/api/v1/endpoints/users.py")
        
        # Create empty endpoints directory
        os.makedirs("app/api/v1/endpoints", exist_ok=True)
        with open("app/api/v1/endpoints/__init__.py", "w") as f:
            f.write("# Import your endpoint routers here\n")
    
    # Remove Docker files if not needed
    if include_docker == "no":
        print("🗑️  Removing Docker files...")
        remove_file_if_exists("Dockerfile")
        remove_file_if_exists("docker-compose.yml")
        remove_file_if_exists(".dockerignore")
    
    # Remove testing files if not needed
    if include_testing == "none":
        print("🗑️  Removing test files...")
        remove_dir_if_exists("tests")
        remove_file_if_exists("pytest.ini")
        remove_file_if_exists("conftest.py")
    
    # Remove GitHub Actions if not needed
    if include_github_actions == "no":
        print("🗑️  Removing GitHub Actions...")
        remove_dir_if_exists(".github")
    
    # Create .env file from template
    print("⚙️  Creating .env file...")
    if os.path.exists("env.example"):
        shutil.copy("env.example", ".env")
        print("✅ Created .env file from env.example")
    
    # Create .gitignore
    print("📝 Creating .gitignore...")
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Database
*.db
*.sqlite3

# Logs
logs/
*.log

# OS
.DS_Store
Thumbs.db

# Alembic
alembic/versions/*.py
!alembic/versions/__init__.py

# Docker
.dockerignore

# Testing
.pytest_cache/
.coverage
htmlcov/

# Local development
.env.local
.env.development
.env.test
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    print("✅ Created .gitignore")
    
    # Initialize git repository
    print("🔧 Initializing git repository...")
    try:
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "branch", "-m", "main"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit from FastAPI Cookiecutter template"], 
                      check=True, capture_output=True)
        print("✅ Git repository initialized with 'main' branch")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Git initialization failed: {e}")
        print("   Make sure git is installed and configured")
    except FileNotFoundError:
        print("⚠️  Git not found. Please install git to initialize repository")
    
    # Create alembic versions directory
    print("📁 Setting up Alembic...")
    versions_dir = Path("alembic/versions")
    versions_dir.mkdir(parents=True, exist_ok=True)
    
    # Create __init__.py in versions directory if it doesn't exist
    init_file = versions_dir / "__init__.py"
    if not init_file.exists():
        init_file.write_text("# Alembic migration versions\n")
    
    print("✅ Alembic setup complete")
    
    # Display completion message and next steps
    print("\n" + "="*60)
    print("🎉 Project generated successfully!")
    print("="*60)
    
    project_name = "{{ cookiecutter.project_name }}"
    print(f"\n📁 Project: {project_name}")
    print(f"📂 Directory: {{ cookiecutter.project_slug }}")
    
    print("\n🚀 Next Steps:")
    print("-" * 20)
    
    if development_environment == "full_docker":
        print("🐳 Full Docker Setup:")
        print("1. docker-compose up")
        print("2. Visit http://localhost:{{ cookiecutter.api_port }}/docs")
        
    elif development_environment == "docker_db_local_app":
        print("🐳 Docker DB + Local App Setup:")
        print("1. python -m venv venv")
        print("2. source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        print("3. pip install -r requirements.txt")
        print("4. docker-compose up db -d")
        print("5. alembic revision --autogenerate -m 'Initial migration'")
        print("6. alembic upgrade head")
        print("7. uvicorn app.main:app --reload")
        print("8. Visit http://localhost:{{ cookiecutter.api_port }}/docs")
        
    else:  # local_development
        print("💻 Local Development Setup:")
        print("1. Create PostgreSQL database: createdb {{ cookiecutter.database_name }}")
        print("2. python -m venv venv")
        print("3. source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        print("4. pip install -r requirements.txt")
        print("5. Edit .env with your database settings")
        print("6. alembic revision --autogenerate -m 'Initial migration'")
        print("7. alembic upgrade head")
        print("8. uvicorn app.main:app --reload")
        print("9. Visit http://localhost:{{ cookiecutter.api_port }}/docs")
    
    print(f"\n📚 Documentation: http://localhost:{{ cookiecutter.api_port }}/docs")
    print("💡 Read the README.md for detailed instructions")
    print("\n✨ Happy coding!")

if __name__ == "__main__":
    main()

