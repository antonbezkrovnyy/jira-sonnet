from fastapi import FastAPI
from .core.config import get_settings

def create_app() -> FastAPI:
    app = FastAPI(title="JIRA Sonnet API")
    
    @app.get("/health")
    async def health_check() -> dict[str, str]:
        settings = get_settings()
        return {"status": "ok"}
    
    return app

app = create_app()