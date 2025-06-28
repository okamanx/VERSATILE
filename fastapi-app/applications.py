from fastapi import APIRouter, HTTPException, Depends, Query
from database import db
from schemas import ApplicationCreate
from auth import verify_player, verify_org
from bson import ObjectId

router = APIRouter()

# PLAYER: Apply to a gig
@router.post("/apply")
async def apply_to_gig(application: ApplicationCreate, current_user: dict = Depends(verify_player)):
    if current_user["user_type"] != "player":
        raise HTTPException(status_code=403, detail="Only players can apply to gigs.")

    existing = await db["applications"].find_one({
        "gig_id": application.gig_id,
        "player_id": current_user["id"],
        "status": {"$ne": "rejected"}  # blocks if not rejected
    })
    if existing:
        raise HTTPException(status_code=400, detail="You have already applied to this gig.")

    app_dict = application.model_dump()
    app_dict["player_id"] = current_user["id"]
    app_dict["status"] = "pending"
    new_app = await db["applications"].insert_one(app_dict)
    return {"id": str(new_app.inserted_id)}


# ORG: View applications for a gig
@router.get("/applications/{gig_id}")
async def view_applications(gig_id: str, current_user: dict = Depends(verify_org)):
    # Make sure gig belongs to this org
    gig = await db["gigs"].find_one({"_id": ObjectId(gig_id)})
    if not gig or gig["org_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="You don't own this gig.")

    applications = []
    async for app in db["applications"].find({"gig_id": gig_id}):
        app["_id"] = str(app["_id"])

        # Fetch player info
        player = await db["users"].find_one({"_id": ObjectId(app["player_id"])})
        if player:
            app["player"] = {
                "id": str(player["_id"]),
                "name": player.get("name") or player.get("username"),
                "email": player.get("email"),
                "user_type": player.get("user_type")
            }

        applications.append(app)

    return applications

# ORG: Delete an application
@router.delete("/applications/{application_id}")
async def delete_application(application_id: str, current_user: dict = Depends(verify_org)):
    application = await db["applications"].find_one({"_id": ObjectId(application_id)})
    if not application:
        raise HTTPException(status_code=404, detail="Application not found.")

    gig = await db["gigs"].find_one({"_id": ObjectId(application["gig_id"])})
    if not gig or gig["org_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="You don't own this gig.")

    await db["applications"].delete_one({"_id": ObjectId(application_id)})
    return {"message": "Application deleted successfully."}

# PLAYER: View own applications with gig info
@router.get("/my_applications")
async def get_my_applications(current_user: dict = Depends(verify_player)):
    applications = []
    async for app in db["applications"].find({"player_id": current_user["id"]}):
        app["_id"] = str(app["_id"])

        # Fetch gig details
        gig = await db["gigs"].find_one({"_id": ObjectId(app["gig_id"])})
        if gig:
            gig["_id"] = str(gig["_id"])
            app["gig"] = {
                "id": gig["_id"],
                "title": gig.get("title"),
                "description": gig.get("description"),
                "org_id": gig.get("org_id")
            }

        applications.append(app)

    return applications

@router.patch("/applications/{application_id}/status")
async def update_application_status(application_id: str, status: str = Query(...), current_user: dict = Depends(verify_org)):
    if status not in ["pending", "accepted", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status value.")

    application = await db["applications"].find_one({"_id": ObjectId(application_id)})
    if not application:
        raise HTTPException(status_code=404, detail="Application not found.")

    gig = await db["gigs"].find_one({"_id": ObjectId(application["gig_id"])})
    if not gig or gig["org_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="You don't own this gig.")

    await db["applications"].update_one({"_id": ObjectId(application_id)}, {"$set": {"status": status}})
    return {"message": f"Application status updated to {status}."}
