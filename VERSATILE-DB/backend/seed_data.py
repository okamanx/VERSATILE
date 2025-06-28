"""
Seed data script for MongoDB VERSATILE-DB
Converted from SQLAlchemy to MongoDB
"""

import asyncio
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timezone
from backend.database import db, test_mongo_connection
from backend.mongo_models import (
    UserModel, ProfileModel, GameModel, HighlightModel, 
    GigModel, ApplicationModel, TeamModel, SponsorModel,
    COLLECTIONS
)

async def seed_data():
    """Seed MongoDB with sample data"""
    
    # Test connection first
    if not await test_mongo_connection():
        print("❌ Cannot connect to MongoDB. Please ensure MongoDB is running.")
        return
    
    try:
        print("🔄 Seeding MongoDB with sample data...")
        
        # Clear existing data
        for collection_name in COLLECTIONS.values():
            await db[collection_name].delete_many({})
        print("✅ Cleared existing data")
        
        # Create users
        users_data = [
            {"email": "john.doe@example.com", "username": "john_doe", "discord_id": "john_doe#1234", "wallet_address": "0x1234567890abcdef"},
            {"email": "jane.smith@example.com", "username": "jane_smith", "discord_id": "jane_smith#5678", "wallet_address": "0xfedcba0987654321"},
            {"email": "bob.wilson@example.com", "username": "bob_wilson", "discord_id": "bob_wilson#9012", "wallet_address": "0xabcdef1234567890"},
            {"email": "alice.johnson@example.com", "username": "alice_j", "discord_id": "alice_j#3456", "wallet_address": "0x9876543210fedcba"},
            {"email": "charlie.brown@example.com", "username": "charlie_b", "discord_id": "charlie_b#7890", "wallet_address": "0x5555666677778888"},
            {"email": "diana.prince@example.com", "username": "diana_p", "discord_id": "diana_p#1111", "wallet_address": "0x1111222233334444"},
            {"email": "edward.norton@example.com", "username": "edward_n", "discord_id": "edward_n#2222", "wallet_address": "0x2222333344445555"},
            {"email": "fiona.gallagher@example.com", "username": "fiona_g", "discord_id": "fiona_g#3333", "wallet_address": "0x3333444455556666"},
            {"email": "george.lucas@example.com", "username": "george_l", "discord_id": "george_l#4444", "wallet_address": "0x4444555566667777"},
            {"email": "helena.bonham@example.com", "username": "helena_b", "discord_id": "helena_b#5555", "wallet_address": "0x5555666677778888"},
            {"email": "ivan.drago@example.com", "username": "ivan_d", "discord_id": "ivan_d#6666", "wallet_address": "0x6666777788889999"},
            {"email": "julia.roberts@example.com", "username": "julia_r", "discord_id": "julia_r#7777", "wallet_address": "0x777788889999aaaa"},
            {"email": "kevin.bacon@example.com", "username": "kevin_b", "discord_id": "kevin_b#8888", "wallet_address": "0x88889999aaaabbbb"},
            {"email": "lisa.simpson@example.com", "username": "lisa_s", "discord_id": "lisa_s#9999", "wallet_address": "0x9999aaaabbbbcccc"},
            {"email": "michael.jordan@example.com", "username": "michael_j", "discord_id": "michael_j#0000", "wallet_address": "0x0000bbbbccccdddd"}
        ]
        
        # Insert users
        users = []
        for user_data in users_data:
            user = UserModel(**user_data)
            result = await db[COLLECTIONS["users"]].insert_one(user.dict())
            user.id = str(result.inserted_id)
            users.append(user)
        
        print(f"✅ Created {len(users)} users")
        
        # Create profiles
        profiles_data = [
            {"user_id": users[0].id, "bio": "Professional gamer and content creator", "region": "North America", "roles": ["DPS", "Support"], "badges": ["Top 500", "Season Champion"], "grind_data": {"hours_played": 1200, "rank": "Diamond"}, "pentagon_data": {"mechanical": 85, "game_sense": 90, "communication": 75, "teamwork": 80, "adaptability": 85}},
            {"user_id": users[1].id, "bio": "Esports enthusiast and team player", "region": "Europe", "roles": ["Tank", "Flex"], "badges": ["Team Captain", "MVP"], "grind_data": {"hours_played": 800, "rank": "Platinum"}, "pentagon_data": {"mechanical": 75, "game_sense": 85, "communication": 90, "teamwork": 95, "adaptability": 80}},
            {"user_id": users[2].id, "bio": "Rising star in competitive gaming", "region": "Asia", "roles": ["DPS", "Tank"], "badges": ["Rookie of the Year"], "grind_data": {"hours_played": 600, "rank": "Gold"}, "pentagon_data": {"mechanical": 90, "game_sense": 70, "communication": 65, "teamwork": 75, "adaptability": 85}},
            {"user_id": users[3].id, "bio": "Strategic mastermind and shot caller", "region": "North America", "roles": ["Support", "Flex"], "badges": ["Shot Caller", "Analyst"], "grind_data": {"hours_played": 1500, "rank": "Masters"}, "pentagon_data": {"mechanical": 70, "game_sense": 95, "communication": 90, "teamwork": 85, "adaptability": 80}},
            {"user_id": users[4].id, "bio": "Aggressive playstyle specialist", "region": "Europe", "roles": ["DPS", "Duelist"], "badges": ["Aggressive Player", "Clutch Master"], "grind_data": {"hours_played": 900, "rank": "Diamond"}, "pentagon_data": {"mechanical": 95, "game_sense": 75, "communication": 60, "teamwork": 70, "adaptability": 90}}
        ]
        
        for profile_data in profiles_data:
            profile = ProfileModel(**profile_data)
            await db[COLLECTIONS["profiles"]].insert_one(profile.dict())
        
        print(f"✅ Created {len(profiles_data)} profiles")
        
        # Create games
        games_data = [
            {"user_id": users[0].id, "game_name": "Overwatch 2", "rank": "Diamond", "winrate": 0.65, "top_roles": ["DPS", "Support"]},
            {"user_id": users[1].id, "game_name": "Valorant", "rank": "Platinum", "winrate": 0.58, "top_roles": ["Controller", "Duelist"]},
            {"user_id": users[2].id, "game_name": "League of Legends", "rank": "Gold", "winrate": 0.52, "top_roles": ["ADC", "Top"]},
            {"user_id": users[3].id, "game_name": "CS:GO", "rank": "Masters", "winrate": 0.72, "top_roles": ["Rifler", "AWP"]},
            {"user_id": users[4].id, "game_name": "Dota 2", "rank": "Diamond", "winrate": 0.61, "top_roles": ["Carry", "Support"]}
        ]
        
        for game_data in games_data:
            game = GameModel(**game_data)
            await db[COLLECTIONS["games"]].insert_one(game.dict())
        
        print(f"✅ Created {len(games_data)} games")
        
        # Create highlights
        highlights_data = [
            {"user_id": users[0].id, "title": "Epic 6K with Genji", "clip_url": "https://youtube.com/watch?v=abc123", "tags": ["genji", "6k", "play_of_the_game"]},
            {"user_id": users[1].id, "title": "Perfect Ace with Sova", "clip_url": "https://youtube.com/watch?v=def456", "tags": ["sova", "ace", "clutch"]},
            {"user_id": users[2].id, "title": "Insane 1v5 Clutch", "clip_url": "https://youtube.com/watch?v=ghi789", "tags": ["clutch", "1v5", "epic"]},
            {"user_id": users[3].id, "title": "Perfect Headshot Sequence", "clip_url": "https://youtube.com/watch?v=jkl012", "tags": ["headshot", "precision", "aim"]},
            {"user_id": users[4].id, "title": "Team Wipe with Ultimate", "clip_url": "https://youtube.com/watch?v=mno345", "tags": ["ultimate", "team_wipe", "combo"]}
        ]
        
        for highlight_data in highlights_data:
            highlight = HighlightModel(**highlight_data)
            await db[COLLECTIONS["highlights"]].insert_one(highlight.dict())
        
        print(f"✅ Created {len(highlights_data)} highlights")
        
        # Create sponsors
        sponsors_data = [
            {"name": "GamingGear Pro", "org_id": "org_001", "verified": True},
            {"name": "EnergyDrink Co", "org_id": "org_002", "verified": False},
            {"name": "Razer Gaming", "org_id": "org_003", "verified": True},
            {"name": "Logitech G", "org_id": "org_004", "verified": True},
            {"name": "SteelSeries", "org_id": "org_005", "verified": True}
        ]
        
        for sponsor_data in sponsors_data:
            sponsor = SponsorModel(**sponsor_data)
            await db[COLLECTIONS["sponsors"]].insert_one(sponsor.dict())
        
        print(f"✅ Created {len(sponsors_data)} sponsors")
        
        # Create gigs
        gigs_data = [
            {"title": "Content Creator for Gaming Channel", "description": "Looking for skilled gamers to create content for our YouTube channel", "org_id": "org_001", "budget": 5000.0, "method": "upi", "status": "open"},
            {"title": "Esports Team Coach", "description": "Experienced coach needed for amateur esports team", "org_id": "org_002", "budget": 3000.0, "method": "card", "status": "open"},
            {"title": "Game Streamer", "description": "Professional streamer needed for daily gaming content", "org_id": "org_003", "budget": 4000.0, "method": "upi", "status": "open"},
            {"title": "Tournament Organizer", "description": "Experienced organizer for online gaming tournaments", "org_id": "org_004", "budget": 2500.0, "method": "card", "status": "open"},
            {"title": "Gaming Analyst", "description": "Analyst needed for esports team performance review", "org_id": "org_005", "budget": 3500.0, "method": "upi", "status": "open"}
        ]
        
        gigs = []
        for gig_data in gigs_data:
            gig = GigModel(**gig_data)
            result = await db[COLLECTIONS["gigs"]].insert_one(gig.dict())
            gig.id = str(result.inserted_id)
            gigs.append(gig)
        
        print(f"✅ Created {len(gigs)} gigs")
        
        # Create applications
        applications_data = [
            {"gig_id": gigs[0].id, "user_id": users[0].id, "resume_link": "https://drive.google.com/resume1", "message": "I have 5 years of content creation experience", "status": "pending"},
            {"gig_id": gigs[1].id, "user_id": users[1].id, "resume_link": "https://drive.google.com/resume2", "message": "Former professional player with coaching experience", "status": "accepted"},
            {"gig_id": gigs[2].id, "user_id": users[2].id, "resume_link": "https://drive.google.com/resume3", "message": "Daily streamer with 10k followers", "status": "pending"},
            {"gig_id": gigs[3].id, "user_id": users[3].id, "resume_link": "https://drive.google.com/resume4", "message": "Organized 50+ tournaments", "status": "rejected"},
            {"gig_id": gigs[4].id, "user_id": users[4].id, "resume_link": "https://drive.google.com/resume5", "message": "Analyst for top esports teams", "status": "pending"}
        ]
        
        for app_data in applications_data:
            application = ApplicationModel(**app_data)
            await db[COLLECTIONS["applications"]].insert_one(application.dict())
        
        print(f"✅ Created {len(applications_data)} applications")
        
        # Create teams
        teams_data = [
            {"name": "Team Elite", "description": "Professional esports team", "captain_id": users[0].id, "members": [users[0].id, users[1].id, users[2].id]},
            {"name": "Gaming Warriors", "description": "Amateur competitive team", "captain_id": users[3].id, "members": [users[3].id, users[4].id]}
        ]
        
        for team_data in teams_data:
            team = TeamModel(**team_data)
            await db[COLLECTIONS["teams"]].insert_one(team.dict())
        
        print(f"✅ Created {len(teams_data)} teams")
        
        # Print summary
        print("\n🎉 MongoDB seeding completed successfully!")
        print("\n📊 Data Summary:")
        for collection_name in COLLECTIONS.values():
            count = await db[collection_name].count_documents({})
            print(f"  - {collection_name}: {count} documents")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(seed_data())
