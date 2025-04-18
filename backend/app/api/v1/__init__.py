from fastapi import APIRouter
from app.api.v1 import tasks, epics, labels, templates, links

api_router = APIRouter()

api_router.include_router(tasks.router)
api_router.include_router(epics.router)
api_router.include_router(labels.router)
api_router.include_router(templates.router)
api_router.include_router(links.router)