from fastapi import APIRouter, HTTPException, Query
from database import db
from bson import ObjectId

router = APIRouter()

@router.post("/mint_soulbound_nft")
async def mint_nft(user_id: str = Query(...)):
    # Check if user exists
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Check if NFT already minted
    existing_nft = await db["soulbound_nfts"].find_one({"user_id": user_id})
    if existing_nft:
        return {
            "message": "NFT already minted.",
            "nft": {
                "user_id": existing_nft["user_id"],
                "name": existing_nft["name"],
                "reputation": existing_nft["reputation"],
                "minted_at": existing_nft["minted_at"]
            }
        }

    # 🔍 Endorsement criteria check
    endorsements_cursor = db["endorsements"].find({"endorsed_id": user_id})
    endorsements = [e async for e in endorsements_cursor]

    if len(endorsements) < 3:
        raise HTTPException(status_code=403, detail="Not enough endorsements to mint NFT.")

    avg_rating = sum(e["rating"] for e in endorsements) / len(endorsements)
    
    if avg_rating >= 4.7:
        reputation = "🥇 Gold SkillLink Talent"
    elif avg_rating >= 4.3:
        reputation = "🥈 Silver SkillLink Talent"
    elif avg_rating >= 4.0:
        reputation = "🥉 Bronze SkillLink Talent"
    else:
        raise HTTPException(status_code=403, detail="Average rating too low to mint NFT.")

    # Simulate NFT metadata
    nft_data = {
        "user_id": user_id,
        "name": user["name"],
        "reputation": reputation,
        "minted_at": str(ObjectId().generation_time)
    }

    await db["soulbound_nfts"].insert_one(nft_data)

    return {
        "message": "Soulbound NFT minted!",
        "nft": nft_data
    }

@router.get("/nft/{user_id}")
async def get_nft(user_id: str):
    nft = await db["soulbound_nfts"].find_one({"user_id": user_id})
    if not nft:
        raise HTTPException(status_code=404, detail="NFT not minted for this user.")
    
    return {
        "user_id": nft["user_id"],
        "name": nft["name"],
        "reputation": nft["reputation"],
        "minted_at": nft["minted_at"]
    }