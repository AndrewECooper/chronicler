"""
The Chronicler - FastAPI Backend
Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(
    title="The Chronicler API",
    description="AI-powered RPG gamemaster experience",
    version="0.1.0"
)

# CORS configuration for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "chronicler-backend"}

# API routes will be added here
@app.get("/api")
async def api_root():
    """API root endpoint"""
    return {
        "message": "The Chronicler API",
        "version": "0.1.0",
        "status": "development"
    }

# Serve static files (Vue frontend) - must be last
# Check multiple possible locations for the frontend dist folder
possible_dist_paths = [
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "frontend", "dist"),  # Development
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "static"),  # Production (Railway)
]

frontend_dist = None
for path in possible_dist_paths:
    if os.path.exists(path):
        frontend_dist = path
        break

if frontend_dist:
    # Mount assets directory if it exists
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve the Vue frontend for all non-API routes"""
        # If the path exists as a file, serve it
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        # Otherwise, serve index.html (for Vue Router)
        index_path = os.path.join(frontend_dist, "index.html")
        if os.path.isfile(index_path):
            return FileResponse(index_path)
        # If no frontend is available, return a simple message
        return {"message": "Frontend not available", "api": "/api"}
