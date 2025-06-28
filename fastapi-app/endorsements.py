from fastapi import APIRouter, HTTPException, Depends, Query
from database import db
from schemas import EndorsementCreate
from auth import get_current_user
from bson import ObjectId
from datetime import datetime

router = APIRouter()

# ORG: Endorse a player
@router.post("/endorse")
async def endorse_user(endorsement: EndorsementCreate, current_user: dict = Depends(get_current_user)):
    if current_user["id"] == endorsement.endorsed_id:
        raise HTTPException(status_code=400, detail="You can't endorse yourself.")

    if current_user["user_type"] != "org":
        raise HTTPException(status_code=403, detail="Only organizations can endorse players.")

    endorse_dict = endorsement.model_dump()
    endorse_dict["endorsed_by"] = current_user["id"]
    endorse_dict["created_at"] = datetime.utcnow()  # ✅ Timestamp for filtering
    new_endorse = await db["endorsements"].insert_one(endorse_dict)
    return {"id": str(new_endorse.inserted_id)}

# ANYONE: View endorsements of a user (usually player)
@router.get("/endorsements/{user_id}")
async def view_endorsements(
    user_id: str,
    page: int = 1,
    limit: int = 10,
    endorsed_by: str = Query(None),
    min_rating: int = Query(None),
    max_rating: int = Query(None),
    created_before: str = Query(None),
    created_after: str = Query(None),
    sort_by: str = Query("created_at"),  # default sorting
    order: str = Query("desc")           # asc or desc
):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page and limit must be positive integers.")

    query_filter = {"endorsed_id": user_id}

    if endorsed_by:
        query_filter["endorsed_by"] = endorsed_by
    if min_rating is not None:
        query_filter["rating"] = {"$gte": min_rating}
    if max_rating is not None:
        query_filter.setdefault("rating", {})["$lte"] = max_rating
    if created_before:
        query_filter["created_at"] = {"$lte": datetime.fromisoformat(created_before)}
    if created_after:
        query_filter.setdefault("created_at", {})["$gte"] = datetime.fromisoformat(created_after)

    # 🧠 Determine sorting field and order
    allowed_sort_fields = {"created_at", "rating"}
    if sort_by not in allowed_sort_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort_by}")

    sort_order = -1 if order.lower() == "desc" else 1

    total = await db["endorsements"].count_documents(query_filter)
    cursor = db["endorsements"].find(query_filter).sort(sort_by, sort_order).skip((page - 1) * limit).limit(limit)

    endorsements = []
    async for endorse in cursor:
        endorse["_id"] = str(endorse["_id"])
        endorsements.append(endorse)

    return {
        "page": page,
        "limit": limit,
        "count": len(endorsements),
        "total": total,
        "results": endorsements
    }

# ORG: Delete own endorsement
@router.delete("/endorsements/{endorsement_id}")
async def delete_endorsement(endorsement_id: str, current_user: dict = Depends(get_current_user)):
    endorsement = await db["endorsements"].find_one({"_id": ObjectId(endorsement_id)})
    if not endorsement:
        raise HTTPException(status_code=404, detail="Endorsement not found.")

    if endorsement["endorsed_by"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="You can only delete your own endorsements.")

    await db["endorsements"].delete_one({"_id": ObjectId(endorsement_id)})
    return {"message": "Endorsement deleted successfully."}
