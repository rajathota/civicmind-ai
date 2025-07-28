#!/usr/bin/env python3
"""
CivicMind AI Framework Installer
===============================

Quick setup script for the CivicMind AI framework.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, cwd=None):
    """Run a shell command and return success status"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True
        )
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error output: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception running command {command}: {e}")
        return False


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Python 3.11 or higher is required")
        print(f"Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor} detected")
    return True


def check_dependencies():
    """Check if required system dependencies are available"""
    dependencies = ['pip', 'git']
    missing = []
    
    for dep in dependencies:
        if not shutil.which(dep):
            missing.append(dep)
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        return False
    
    print("✅ System dependencies available")
    return True


def setup_virtual_environment():
    """Create and activate virtual environment"""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    print("📦 Creating virtual environment...")
    if not run_command(f"{sys.executable} -m venv venv"):
        return False
    
    print("✅ Virtual environment created")
    return True


def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python packages...")
    
    # Determine pip path based on OS
    if os.name == 'nt':  # Windows
        pip_path = "venv\\Scripts\\pip"
    else:  # Unix-like
        pip_path = "venv/bin/pip"
    
    commands = [
        f"{pip_path} install --upgrade pip",
        f"{pip_path} install -r requirements.txt"
    ]
    
    for command in commands:
        if not run_command(command):
            return False
    
    print("✅ Python packages installed")
    return True


def setup_environment():
    """Setup environment configuration"""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ Environment file already exists")
        return True
    
    if env_example.exists():
        print("📝 Creating environment file...")
        shutil.copy(env_example, env_file)
        print("✅ Environment file created from template")
        print("⚠️  Please edit .env file with your API keys")
        return True
    
    print("❌ .env.example file not found")
    return False


def create_data_directories():
    """Create necessary data directories"""
    directories = [
        "data",
        "data/vectorstore",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Data directories created")
    return True


def run_tests():
    """Run basic tests to verify installation"""
    print("🧪 Running basic tests...")
    
    if os.name == 'nt':  # Windows
        python_path = "venv\\Scripts\\python"
    else:  # Unix-like
        python_path = "venv/bin/python"
    
    # Test import
    test_command = f'{python_path} -c "import civicmind; print(\\"CivicMind import successful\\")"'
    
    if not run_command(test_command):
        print("❌ Import test failed")
        return False
    
    print("✅ Basic tests passed")
    return True


def print_next_steps():
    """Print instructions for next steps"""
    print("\n" + "="*60)
    print("🎉 CivicMind AI Framework Setup Complete!")
    print("="*60)
    print("\n📋 Next Steps:")
    print("\n1. Configure your environment:")
    print("   - Edit .env file with your OpenAI API key")
    print("   - Optionally add LangSmith API key for debugging")
    
    print("\n2. Start the server:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\python server.py")
    else:
        print("   source venv/bin/activate")
        print("   python server.py")
    
    print("\n3. Test the API:")
    print("   curl http://localhost:8000/health")
    
    print("\n4. View documentation:")
    print("   - API docs: http://localhost:8000/docs")
    print("   - Quick start: docs/quickstart.md")
    print("   - Architecture: docs/architecture.md")
    
    print("\n5. Customize for your location:")
    print("   - Add local civic data sources")
    print("   - Customize agent prompts")
    print("   - Configure government API integrations")
    
    print("\n📚 Resources:")
    print("   - GitHub: https://github.com/your-repo/civicmind")
    print("   - Documentation: ./docs/")
    print("   - Examples: ./examples/")


def main():
    """Main setup function"""
    print("🚀 CivicMind AI Framework Setup")
    print("=" * 40)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_dependencies():
        sys.exit(1)
    
    # Setup steps
    steps = [
        ("Setting up virtual environment", setup_virtual_environment),
        ("Installing requirements", install_requirements),
        ("Setting up environment", setup_environment),
        ("Creating data directories", create_data_directories),
        ("Running tests", run_tests)
    ]
    
    for step_name, step_function in steps:
        print(f"\n{step_name}...")
        if not step_function():
            print(f"❌ Failed: {step_name}")
            sys.exit(1)
    
    print_next_steps()


if __name__ == "__main__":
    main()
