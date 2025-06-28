def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "user_type": user["user_type"]
    }

def gig_helper(gig):
    return {
        "id": str(gig["_id"]),
        "title": gig.get("title"),
        "description": gig.get("description"),
        "location": gig.get("location"),
        "game": gig.get("game"),
        "budget": gig.get("budget"),
        "skills_required": gig.get("skills_required"),
        "tags": gig.get("tags", []),
        "deadline": gig.get("deadline"),
        "status": gig.get("status", "open"),
        "org_id": gig.get("org_id"),
        "created_at": gig.get("created_at"),
        "applicant_count": gig.get("applicant_count", 0)
    }

def multiple_gigs_helper(gigs):
    return [gig_helper(g) for g in gigs]

def application_helper(app) -> dict:
    return {
        "id": str(app["_id"]),
        "gig_id": app["gig_id"],
        "player_id": app["player_id"],
        "status": app.get("status", "pending")
    }

def endorsement_helper(endorsement) -> dict:
    return {
        "id": str(endorsement["_id"]),
        "endorsed_id": endorsement["endorsed_id"],
        "endorsed_by": endorsement["endorsed_by"],
        "message": endorsement["message"]
    }