from fastapi import FastAPI
from app.api.v1 import api_router

def create_app() -> FastAPI:
    app = FastAPI(title="JIRA Sonnet API")
    
    # Include main API router
    app.include_router(api_router)
    
    @app.get("/health")
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}
    
    return app

app = create_app()