from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import auth, keys, hsm_config
from app.models.database import create_tables
import os

# Create database tables on startup
create_tables()

app = FastAPI(
    title="CloudHSM Management Dashboard API",
    description="API for managing AWS CloudHSM operations",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    
)


# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(keys.router, prefix="/api/v1")
app.include_router(hsm_config.router, prefix="/api/v1")

# Mount static files for React frontend
if os.path.exists("../build"):
    app.mount("/static", StaticFiles(directory="../build/static"), name="static")
    
    @app.get("/")
    async def serve_frontend():
        return FileResponse("../build/index.html")
    
    @app.get("/{path:path}")
    async def serve_frontend_routes(path: str):
        # Serve React app for all non-API routes
        if not path.startswith("api/") and not path.startswith("health"):
            return FileResponse("../build/index.html")
        # For API routes, let FastAPI's 404 handler take over
        raise HTTPException(status_code=404, detail="Not found")



@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "cloudhsm-dashboard-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)