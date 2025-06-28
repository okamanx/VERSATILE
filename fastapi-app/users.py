from fastapi import APIRouter, HTTPException, Depends
from database import db
from schemas import UserCreate, UserOut, UserLogin, UserUpdate
from auth import hash_password, verify_password, create_access_token, get_current_user
from models import user_helper
from bson import ObjectId
router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register_user(user: UserCreate):
    user_exists = await db["users"].find_one({"email": user.email})
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered.")
    
    user_dict = user.model_dump()
    user_dict["password"] = hash_password(user_dict["password"])
    new_user = await db["users"].insert_one(user_dict)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})
    return user_helper(created_user)

@router.post("/login")
async def login(user: UserLogin):
    user_from_db = await db["users"].find_one({"email": user.email})
    if not user_from_db:
        raise HTTPException(status_code=404, detail="User not found.")
    
    if not verify_password(user.password, user_from_db["password"]):
        raise HTTPException(status_code=401, detail="Incorrect password.")
    
    token = create_access_token({"id": str(user_from_db["_id"]), "email": user_from_db["email"], "user_type": user_from_db["user_type"]})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
async def get_my_profile(current_user: dict = Depends(get_current_user)):
    return current_user

@router.get("/users/{user_id}")
async def get_user_profile(user_id: str):
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    public_fields = {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "user_type": user["user_type"]
    }
    return public_fields

@router.get("/orgs/{org_id}")
async def get_org_profile(org_id: str):
    user = await db["users"].find_one({"_id": ObjectId(org_id)})
    if not user or user["user_type"] != "org":
        raise HTTPException(status_code=404, detail="Organization not found.")

    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "user_type": user["user_type"]
    }

@router.patch("/me")
async def update_my_profile(update: UserUpdate, current_user: dict = Depends(get_current_user)):
    update_data = {k: v for k, v in update.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update.")

    await db["users"].update_one({"_id": ObjectId(current_user["id"])}, {"$set": update_data})
    updated_user = await db["users"].find_one({"_id": ObjectId(current_user["id"])})
    return user_helper(updated_user)

@router.get("/admin/stats")
async def get_admin_stats():
    users_total = await db["users"].count_documents({})
    players = await db["users"].count_documents({"user_type": "player"})
    orgs = await db["users"].count_documents({"user_type": "org"})
    gigs = await db["gigs"].count_documents({})
    applications = await db["applications"].count_documents({})
    endorsements = await db["endorsements"].count_documents({})
    nfts = await db["soulbound_nfts"].count_documents({})

    return {
        "users_total": users_total,
        "players": players,
        "orgs": orgs,
        "gigs": gigs,
        "applications": applications,
        "endorsements": endorsements,
        "nfts_minted": nfts
    }
