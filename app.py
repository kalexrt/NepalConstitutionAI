from fastapi import FastAPI

from nepal_constitution_ai.routes.routes import router as api_router

__app_name__ = "Nepal Constitution AI REST API"
__version__ = "1.0.0"
app = FastAPI(title=__app_name__)


# Initialize Routes
@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {"app": __app_name__, "version": __version__}
# Include the router
app.include_router(api_router, prefix="/api/v1")

__all__ = ["app"]