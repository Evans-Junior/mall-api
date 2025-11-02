from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from data import malls

app = FastAPI(
    title="Ghana Mall API",
    description="API for retrieving mall names, cities, and rankings in Ghana",
    version="1.0.0"
)


origins = [
    "*",    # ⚠️ allow all domains
    # "http://localhost:3000",
    # "http://127.0.0.1:5500",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # domains allowed
    allow_credentials=True,
    allow_methods=["*"],         # GET, POST, PUT, DELETE
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the Ghana Mall API"}


# ✅ Get all malls
@app.get("/malls")
def get_malls():
    return malls


# ✅ Get mall by ID
@app.get("/mall/{mall_id}")
def get_mall(mall_id: int):
    mall = next((m for m in malls if m["id"] == mall_id), None)
    if not mall:
        raise HTTPException(status_code=404, detail="Mall not found")
    return mall


# ✅ Get all mall names
@app.get("/malls/names")
def get_mall_names():
    return [m["name"] for m in malls]


# ✅ Get malls by class/rank
@app.get("/malls/class/{rank}")
def get_malls_by_rank(rank: str):
    result = [m for m in malls if m["rank"].lower() == rank.lower()]
    if not result:
        raise HTTPException(status_code=404, detail="No malls found in this class")
    return result


# ✅ Get list of all available ranks
@app.get("/malls/classes")
def get_all_ranks():
    return list(set(m["rank"] for m in malls))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
