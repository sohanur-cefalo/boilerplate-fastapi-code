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
from pathlib import Path

def main():
    if len(sys.argv) != 2:
        print("❌ Usage: python start_project.py <project_name>")
        print("Example: python start_project.py my_awesome_api")
        sys.exit(1)
    
    project_name = sys.argv[1]
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
            '__pycache__', '*.pyc', '.git', '.DS_Store', 'alembic/versions/*.py'
        ))
        
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
        
        # Update README
        print("📝 Updating README...")
        readme_file = project_dir / "README.md"
        if readme_file.exists():
            content = readme_file.read_text()
            content = content.replace(
                "# FastAPI Boilerplate with SQLAlchemy 2.0",
                f"# {project_name.replace('_', ' ').title()}"
            )
            readme_file.write_text(content)
        
        # Initialize git repository
        print("🔧 Initializing git repository...")
        try:
            subprocess.run(["git", "init"], cwd=project_dir, check=True)
            subprocess.run(["git", "add", "."], cwd=project_dir, check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit from FastAPI boilerplate"], cwd=project_dir, check=True)
            print("✅ Git repository initialized")
        except subprocess.CalledProcessError:
            print("⚠️  Git initialization failed (git might not be installed)")
        
        print("\n" + "="*60)
        print("🎉 Project created successfully!")
        print("="*60)
        print(f"\n📁 Project location: {project_dir}")
        print("\n📋 Next steps:")
        print("1. cd " + str(project_dir))
        print("2. cp env.example .env")
        print("3. Edit .env with your database settings")
        print("4. pip install -r requirements.txt")
        print("5. alembic revision --autogenerate -m 'Initial migration'")
        print("6. alembic upgrade head")
        print("7. uvicorn app.main:app --reload")
        print("\n🌐 Visit http://localhost:8000/docs for API documentation")
        print("\n🐚 Use interactive shell: python management/shell_launcher.py bpython")
        print("\n📚 Read README.md for detailed instructions")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error creating project: {e}")
        if project_dir.exists():
            shutil.rmtree(project_dir)
        sys.exit(1)

if __name__ == "__main__":
    main()
