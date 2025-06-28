from fastapi import APIRouter, HTTPException, Depends, Query
from database import db
from schemas import GigCreate, GigOut
from bson import ObjectId
from auth import verify_org
from models import gig_helper, multiple_gigs_helper
from datetime import datetime

router = APIRouter()

@router.get("/gigs")
async def browse_gigs(
    page: int = 1,
    limit: int = 10,
    title: str = Query(None),
    location: str = Query(None),
    org_id: str = Query(None),
    search: str = Query(None),
    tag: str = Query(None),
    status: str = Query(None),
    sort_by: str = Query("created_at"),
    order: str = Query("desc")
):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page and limit must be positive integers.")

    allowed_sort_fields = {"created_at", "title"}
    if sort_by not in allowed_sort_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort_by}")
    sort_order = -1 if order.lower() == "desc" else 1

    # Auto-close expired gigs (every time browse is triggered)
    await db["gigs"].update_many(
        {"deadline": {"$lt": datetime.utcnow()}, "status": "open"},
        {"$set": {"status": "closed"}}
    )

    query_filter = {}
    if title:
        query_filter["title"] = {"$regex": title, "$options": "i"}
    if location:
        query_filter["location"] = {"$regex": location, "$options": "i"}
    if org_id:
        query_filter["org_id"] = org_id
    if tag:
        query_filter["tags"] = tag.lower()
    if status:
        query_filter["status"] = status.lower()
    if search:
        query_filter["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]

    gigs_cursor = (
        db["gigs"]
        .find(query_filter)
        .sort(sort_by, sort_order)
        .skip((page - 1) * limit)
        .limit(limit)
    )

    gigs = []
    async for gig in gigs_cursor:
        gig["_id"] = str(gig["_id"])
        # Get applicant count
        count = await db["applications"].count_documents({"gig_id": gig["_id"]})
        gig["applicant_count"] = count
        gigs.append(gig)

    total = await db["gigs"].count_documents(query_filter)

    return {
        "page": page,
        "limit": limit,
        "count": len(gigs),
        "total": total,
        "results": multiple_gigs_helper(gigs)
    }

@router.get("/my_gigs")
async def get_my_gigs(
    current_user: dict = Depends(verify_org),
    page: int = 1,
    limit: int = 10
):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page and limit must be positive integers.")

    query_filter = {"org_id": current_user["id"]}
    total = await db["gigs"].count_documents(query_filter)
    gigs_cursor = db["gigs"].find(query_filter).skip((page - 1) * limit).limit(limit)

    gigs = []
    async for gig in gigs_cursor:
        gig["_id"] = str(gig["_id"])
        gigs.append(gig)

    return {
        "page": page,
        "limit": limit,
        "count": len(gigs),
        "total": total,
        "results": gig_helper(gigs)
    }

@router.patch("/gigs/{gig_id}")
async def update_gig(
    gig_id: str,
    updated_data: dict,
    current_user: dict = Depends(verify_org)  
):
    gig = await db["gigs"].find_one({"_id": ObjectId(gig_id)})
    if not gig:
        raise HTTPException(status_code=404, detail="Gig not found.")
    if gig["org_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Unauthorized to edit this gig.")

    allowed_fields = [
        "title", "description", "location", "game", "budget", "skills_required",
        "tags", "deadline", "status"
    ]

    filtered_data = {k: v for k, v in updated_data.items() if k in allowed_fields}

    if not filtered_data:
        raise HTTPException(status_code=400, detail="No valid fields to update.")

    await db["gigs"].update_one({"_id": ObjectId(gig_id)}, {"$set": filtered_data})
    return {"message": "Gig updated successfully."}

@router.delete("/gigs/{gig_id}")
async def delete_gig(
    gig_id: str,
    current_user: dict = Depends(verify_org)
):
    gig = await db["gigs"].find_one({"_id": ObjectId(gig_id)})
    if not gig:
        raise HTTPException(status_code=404, detail="Gig not found.")
    if gig["org_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this gig.")

    await db["gigs"].delete_one({"_id": ObjectId(gig_id)})
    return {"message": "Gig deleted successfully."}

@router.post("/gigs", response_model=GigOut)
async def post_gig(
    gig: GigCreate,
    current_user: dict = Depends(verify_org) 
):
    gig_dict = gig.model_dump()
    gig_dict["org_id"] = current_user["id"]
    gig_dict["created_at"] = datetime.utcnow()
    gig_dict["tags"] = [t.lower() for t in gig_dict.get("tags", [])]
    gig_dict["status"] = gig_dict.get("status", "open")
    new_gig = await db["gigs"].insert_one(gig_dict)
    created_gig = await db["gigs"].find_one({"_id": new_gig.inserted_id})
    return gig_helper(created_gig)

@router.get("/gigs/{gig_id}", response_model=GigOut)
async def get_gig_detail(gig_id: str):
    gig = await db["gigs"].find_one({"_id": ObjectId(gig_id)})
    if not gig:
        raise HTTPException(status_code=404, detail="Gig not found.")
    return gig_helper(gig)
