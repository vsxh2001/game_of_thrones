from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router

app = FastAPI(
    title="Game of Thrones Championship API",
    description="API for managing the Sword Fighting Championship",
    version="1.0.0",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "Game of Thrones Championship API",
        "docs_url": "/docs",
        "version": "1.0.0",
    }
