from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from data import malls

app = FastAPI(
    title="Ghana Mall API",
    description="API for retrieving mall names, cities, and rankings in Ghana",
    version="1.0.0"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to the Ghana Mall API"}


@app.get("/malls")
def get_malls():
    return malls


@app.get("/mall/{mall_id}")
def get_mall(mall_id: int):
    mall = next((m for m in malls if m["id"] == mall_id), None)
    if not mall:
        raise HTTPException(status_code=404, detail="Mall not found")
    return mall


@app.get("/malls/names")
def get_mall_names():
    return [m["name"] for m in malls]


@app.get("/malls/class/{rank}")
def get_malls_by_rank(rank: str):
    result = [m for m in malls if m["rank"].lower() == rank.lower()]
    if not result:
        raise HTTPException(status_code=404, detail="No malls found in this class")
    return result


@app.get("/malls/classes")
def get_all_ranks():
    return list(set(m["rank"] for m in malls))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
