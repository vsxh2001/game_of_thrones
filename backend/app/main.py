from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.api import api_router

app = FastAPI(title="Game of Thrones Championship API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include API router
app.include_router(api_router, prefix="/api/v1")
