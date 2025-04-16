from fastapi import FastAPI
from .core.config import get_settings
from .api.v1.tasks import router as tasks_router
from .api.v1.epics import router as epics_router

def create_app() -> FastAPI:
    app = FastAPI(title="JIRA Sonnet API")
    
    # Include routers
    app.include_router(tasks_router)
    app.include_router(epics_router)
    
    @app.get("/health")
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}
    
    return app

app = create_app()