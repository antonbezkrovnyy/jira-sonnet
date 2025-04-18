from fastapi import FastAPI
from .api.v1.tasks import router as tasks_router
from .api.v1.epics import router as epics_router
from .api.v1.labels import router as labels_router
from .api.v1.templates import router as templates_router
from .api.v1.links import router as links_router  # Add import

def create_app() -> FastAPI:
    app = FastAPI(title="JIRA Sonnet API")
    
    # Include routers
    app.include_router(tasks_router)
    app.include_router(epics_router)
    app.include_router(labels_router)
    app.include_router(templates_router)
    app.include_router(links_router)  # Add links router
    
    @app.get("/health")
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}
    
    return app

app = create_app()