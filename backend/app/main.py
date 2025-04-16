from fastapi import FastAPI
from .core.config import get_settings
from .api.v1.tasks import router as tasks_router

def create_app() -> FastAPI:
    app = FastAPI(title="JIRA Sonnet API")
    
    # Include routers
    app.include_router(tasks_router)
    
    @app.get("/health")
    async def health_check() -> dict[str, str]:
        settings = get_settings()
        return {"status": "ok"}
    
    return app

app = create_app()