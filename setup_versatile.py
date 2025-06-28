#!/usr/bin/env python3
"""
Unified Setup Script for VERSATILE System
Installs dependencies and sets up both FastAPI app and VERSATILE-DB
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"   ✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ {description} failed: {e}")
        print(f"   Error output: {e.stderr}")
        return False

def install_dependencies():
    """Install all dependencies from unified requirements.txt"""
    print("📦 Installing VERSATILE dependencies...")
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("   ❌ requirements.txt not found in current directory")
        return False
    
    # Install dependencies
    success = run_command("pip install -r requirements.txt", "Installing Python dependencies")
    return success

def setup_database():
    """Setup MongoDB database"""
    print("\n🗄️ Setting up database...")
    
    # Check if we're in the right directory
    if not os.path.exists("fastapi-app"):
        print("   ❌ fastapi-app directory not found")
        return False
    
    # Change to fastapi-app directory and run setup
    os.chdir("fastapi-app")
    success = run_command("python setup_database.py", "Setting up MongoDB database")
    os.chdir("..")
    return success

def validate_configuration():
    """Validate the global configuration"""
    print("\n🔍 Validating configuration...")
    
    try:
        # Import and validate config
        from config import validate_config, display_config
        display_config()
        return validate_config()
    except ImportError as e:
        print(f"   ❌ Configuration validation failed: {e}")
        return False

def create_env_file():
    """Create .env file with default configuration"""
    print("\n📝 Creating .env file...")
    
    env_content = """# VERSATILE Configuration
# Database Configuration
MONGO_URL=mongodb://localhost:27017
MONGO_DB_NAME=versatile_db
SQLALCHEMY_DATABASE_URL=sqlite:///versatile_db.sqlite

# FastAPI Configuration
FASTAPI_HOST=127.0.0.1
FASTAPI_PORT=8000
FASTAPI_RELOAD=True

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Debug Configuration
DEBUG=True
"""
    
    try:
        with open(".env", "w") as f:
            f.write(env_content)
        print("   ✅ .env file created successfully")
        return True
    except Exception as e:
        print(f"   ❌ Failed to create .env file: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 VERSATILE System Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Create .env file if it doesn't exist
    if not os.path.exists(".env"):
        if not create_env_file():
            return False
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Dependency installation failed")
        return False
    
    # Validate configuration
    if not validate_configuration():
        print("❌ Configuration validation failed")
        return False
    
    # Setup database
    if not setup_database():
        print("❌ Database setup failed")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 VERSATILE System Setup Complete!")
    print("=" * 50)
    print("\n📋 Next Steps:")
    print("   1. Start MongoDB (if not already running)")
    print("   2. Start FastAPI server: uvicorn fastapi-app.main:app --reload")
    print("   3. Access API docs: http://127.0.0.1:8000/docs")
    print("   4. Run tests: python fastapi-app/test_all_endpoints.py")
    print("\n🔧 Configuration:")
    print("   - Edit .env file to customize settings")
    print("   - Check config.py for all available options")
    print("\n📚 Documentation:")
    print("   - API endpoints: fastapi-app/api_endpoints.md")
    print("   - Database schema: VERSATILE-DB/README.md")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)
    else:
        print("\n✅ Setup completed successfully!") 