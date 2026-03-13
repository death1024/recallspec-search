from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import search, watchlist, share

app = FastAPI(title="RecallSpec Search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router)
app.include_router(watchlist.router)
app.include_router(share.router)

@app.get("/")
async def root():
    return {"message": "RecallSpec Search API", "version": "0.1.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
