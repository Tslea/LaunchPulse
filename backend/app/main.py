from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import deployments, health, ideas, landing_pages, leads, pipeline


def create_app() -> FastAPI:
    application = FastAPI(
        title="LaunchPulse",
        description="Automated idea validation pipeline — from concept to market data in 24 hours",
        version="0.1.0",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(health.router)
    application.include_router(ideas.router, prefix="/api/v1", tags=["ideas"])
    application.include_router(pipeline.router, prefix="/api/v1", tags=["pipeline"])
    application.include_router(
        landing_pages.router, prefix="/api/v1", tags=["landing-pages"]
    )
    application.include_router(
        deployments.router, prefix="/api/v1", tags=["deployments"]
    )
    application.include_router(leads.router, prefix="/api/v1", tags=["leads"])

    return application


app = create_app()
