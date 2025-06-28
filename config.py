#!/usr/bin/env python3
"""
Global Configuration for VERSATILE System
Centralized configuration for both FastAPI app and VERSATILE-DB
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

# MongoDB Configuration
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "versatile_db")

# SQLAlchemy Configuration (for VERSATILE-DB)
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///versatile_db.sqlite")

# ============================================================================
# FASTAPI CONFIGURATION
# ============================================================================

# Server Configuration
FASTAPI_HOST = os.getenv("FASTAPI_HOST", "127.0.0.1")
FASTAPI_PORT = int(os.getenv("FASTAPI_PORT", "8000"))
FASTAPI_RELOAD = os.getenv("FASTAPI_RELOAD", "True").lower() == "true"

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "SkillLink-secret")
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # 24 hours

# ============================================================================
# APPLICATION CONSTANTS
# ============================================================================

# User Types
USER_TYPE_PLAYER = "player"
USER_TYPE_ORG = "org"
USER_TYPE_ADMIN = "admin"

# Gig Status
GIG_STATUS_OPEN = "open"
GIG_STATUS_CLOSED = "closed"

# Application Status
APPLICATION_STATUS_PENDING = "pending"
APPLICATION_STATUS_ACCEPTED = "accepted"
APPLICATION_STATUS_REJECTED = "rejected"

# NFT Reputation Levels
NFT_REPUTATION_GOLD = "🥇 Gold SkillLink Talent"
NFT_REPUTATION_SILVER = "🥈 Silver SkillLink Talent"
NFT_REPUTATION_BRONZE = "🥉 Bronze SkillLink Talent"

# Reputation Messages
REPUTATION_MESSAGE = "Endorsed SkillLink Talent 💎"

# ============================================================================
# EXTERNAL API CONFIGURATION
# ============================================================================

# OpenDota API for Dota 2 stats
OPENDOTA_API_URL = "https://api.opendota.com/api/players/"

# ============================================================================
# DATABASE COLLECTIONS
# ============================================================================

# MongoDB Collections
COLLECTIONS = {
    "users": "users",
    "profiles": "profiles",
    "games": "games",
    "highlights": "highlights",
    "gigs": "gigs",
    "applications": "applications",
    "endorsements": "endorsements",
    "soulbound_nfts": "soulbound_nfts",
    "teams": "teams",
    "sponsors": "sponsors"
}

# ============================================================================
# VALIDATION CONSTANTS
# ============================================================================

# Rating Range
MIN_RATING = 1
MAX_RATING = 5

# NFT Requirements
MIN_ENDORSEMENTS_FOR_NFT = 3
MIN_AVG_RATING_FOR_NFT = 4.0

# ============================================================================
# DEBUG CONFIGURATION
# ============================================================================

DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# ============================================================================
# CONFIGURATION VALIDATION
# ============================================================================

def validate_config():
    """Validate configuration settings"""
    errors = []
    
    # Validate MongoDB URL
    if not MONGO_URL:
        errors.append("MONGO_URL is not set")
    
    # Validate JWT Secret
    if JWT_SECRET_KEY == "SkillLink-secret" and not DEBUG:
        errors.append("JWT_SECRET_KEY should be changed in production")
    
    # Validate Port
    if not (1024 <= FASTAPI_PORT <= 65535):
        errors.append(f"FASTAPI_PORT {FASTAPI_PORT} is not in valid range (1024-65535)")
    
    if errors:
        print("⚠️ Configuration validation errors:")
        for error in errors:
            print(f"   - {error}")
        return False
    
    print("✅ Configuration validation passed")
    return True

# ============================================================================
# CONFIGURATION DISPLAY
# ============================================================================

def display_config():
    """Display current configuration"""
    print("🔧 VERSATILE Configuration")
    print("=" * 50)
    print(f"📊 Database: {MONGO_DB_NAME}")
    print(f"🔗 MongoDB URL: {MONGO_URL}")
    print(f"🌐 FastAPI Host: {FASTAPI_HOST}")
    print(f"🚪 FastAPI Port: {FASTAPI_PORT}")
    print(f"🔄 Auto Reload: {FASTAPI_RELOAD}")
    print(f"🐛 Debug Mode: {DEBUG}")
    print("=" * 50)

if __name__ == "__main__":
    display_config()
    validate_config() 