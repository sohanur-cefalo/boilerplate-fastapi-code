#!/usr/bin/env python3
"""
Test script for the FastAPI Cookiecutter template.
This script tests various template configurations to ensure they work correctly.
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def test_template_generation(config):
    """Test template generation with specific configuration"""
    print(f"\n🧪 Testing configuration: {config['name']}")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create cookiecutter config file
        config_content = "default_context:\n"
        for key, value in config["context"].items():
            config_content += f"  {key}: {value}\n"
        
        config_file = Path(temp_dir) / "config.yml"
        config_file.write_text(config_content)
        
        # Generate project
        template_dir = Path(__file__).parent
        success, output = run_command(
            f"cookiecutter {template_dir} --config-file {config_file} --no-input -o {temp_dir}"
        )
        
        if not success:
            print(f"❌ Template generation failed: {output}")
            return False
        
        # Find generated project directory
        project_dirs = [d for d in Path(temp_dir).iterdir() if d.is_dir() and d.name != "__pycache__"]
        if not project_dirs:
            print("❌ No project directory found")
            return False
        
        project_dir = project_dirs[0]
        print(f"✅ Generated project in: {project_dir.name}")
        
        # Test basic structure
        required_files = [
            "app/main.py",
            "app/core/config.py",
            "requirements.txt",
            "README.md",
            ".env",
            ".gitignore"
        ]
        
        for file_path in required_files:
            if not (project_dir / file_path).exists():
                print(f"❌ Missing required file: {file_path}")
                return False
        
        print("✅ All required files present")
        
        # Test Python syntax
        success, output = run_command("python -m py_compile app/main.py", cwd=project_dir)
        if not success:
            print(f"❌ Python syntax error in main.py: {output}")
            return False
        
        print("✅ Python syntax valid")
        return True

def main():
    """Main test function"""
    print("🍪 Testing FastAPI Cookiecutter Template")
    print("=" * 50)
    
    # Check if cookiecutter is installed
    success, _ = run_command("cookiecutter --version")
    if not success:
        print("❌ Cookiecutter not installed. Install with: pip install cookiecutter")
        return
    
    # Test configurations
    test_configs = [
        {
            "name": "Minimal API",
            "context": {
                "project_name": "Test Minimal API",
                "include_user_model": "no",
                "include_authentication": "none",
                "development_environment": "full_docker",
                "include_testing": "none",
                "include_github_actions": "no"
            }
        },
        {
            "name": "Full Featured",
            "context": {
                "project_name": "Test Full API",
                "include_user_model": "yes",
                "include_authentication": "jwt",
                "development_environment": "docker_db_local_app",
                "include_testing": "pytest",
                "include_github_actions": "yes"
            }
        },
        {
            "name": "Local Development",
            "context": {
                "project_name": "Test Local API",
                "include_user_model": "yes",
                "include_authentication": "basic",
                "development_environment": "local_development",
                "include_testing": "pytest",
                "include_docker": "no"
            }
        }
    ]
    
    # Run tests
    passed = 0
    total = len(test_configs)
    
    for config in test_configs:
        if test_template_generation(config):
            passed += 1
    
    # Results
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} configurations passed")
    
    if passed == total:
        print("🎉 All tests passed! Template is working correctly.")
    else:
        print("❌ Some tests failed. Please check the template configuration.")

if __name__ == "__main__":
    main()
