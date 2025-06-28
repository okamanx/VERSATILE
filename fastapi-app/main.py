from fastapi import FastAPI
import users, gigs, applications, endorsements, nft

app = FastAPI()

# Routers
app.include_router(users.router)
app.include_router(gigs.router)
app.include_router(applications.router)
app.include_router(endorsements.router)
app.include_router(nft.router)

@app.get("/")
def root():
    return {"message": "SkillLink Backend Running"}