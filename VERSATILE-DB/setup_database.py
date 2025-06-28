#!/usr/bin/env python3
"""
Setup script for VERSATILE-DB MongoDB
Converted from PostgreSQL to MongoDB
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.append(str(Path(__file__).parent / "backend"))

async def setup_mongodb():
    """Setup MongoDB database"""
    print("🔄 Setting up MongoDB database...")
    
    try:
        # Import MongoDB modules
        from backend.database import test_mongo_connection
        from backend.seed_data import seed_data
        
        # Test connection
        if not await test_mongo_connection():
            print("❌ Cannot connect to MongoDB. Please ensure MongoDB is running.")
            return False
        
        # Seed data
        await seed_data()
        
        print("✅ MongoDB setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up MongoDB: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    # Install MongoDB dependencies
    os.system("pip install motor==3.3.2 pymongo==4.6.0 python-dotenv==1.0.0")
    
    print("✅ Dependencies installed")

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    if not env_file.exists():
        env_content = """# MongoDB Configuration
MONGO_URL=mongodb://localhost:27017
MONGO_DB_NAME=versatile_db

# App Configuration
DEBUG=True
"""
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ Created .env file")

async def main():
    """Main setup function"""
    print("🚀 Setting up VERSATILE-DB with MongoDB...")
    
    # Create environment file
    create_env_file()
    
    # Install dependencies
    install_dependencies()
    
    # Setup MongoDB
    success = await setup_mongodb()
    
    if success:
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. MongoDB is ready to use")
        print("2. Database: versatile_db")
        print("3. Collections: users, profiles, games, highlights, gigs, applications, teams, sponsors")
        print("4. You can now use the database with your applications")
    else:
        print("\n❌ Setup failed")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 