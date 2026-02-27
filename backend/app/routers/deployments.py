from fastapi import APIRouter, Depends, HTTPException

from app.clients.vercel_client import VercelClient
from app.dependencies import get_supabase, get_vercel_client
from app.services.deploy_service import DeployService
from app.services.idea_service import IdeaService
from app.services.landing_service import LandingService

router = APIRouter()


@router.post("/ideas/{idea_id}/deploy")
async def deploy_landing_page(
    idea_id: str,
    variant: str = "A",
    vercel: VercelClient = Depends(get_vercel_client),
    supabase=Depends(get_supabase),
):
    """Deploy a generated landing page to Vercel."""
    idea_service = IdeaService(supabase)
    idea = idea_service.get_idea(idea_id)

    landing_service = LandingService(claude=None, supabase=supabase)
    page = landing_service.get_landing_page(idea_id, variant)
    if not page:
        raise HTTPException(
            status_code=400, detail="Landing page not found. Generate it first."
        )

    deploy_service = DeployService(vercel, supabase)
    result = await deploy_service.deploy_landing(
        idea_id=idea_id,
        idea_name=idea.idea_card.name,
        html_content=page["html"],
        landing_page_id=page["id"],
        variant=variant,
    )

    return result


@router.get("/ideas/{idea_id}/deployments")
def list_deployments(
    idea_id: str,
    supabase=Depends(get_supabase),
):
    """List all deployments for an idea."""
    deploy_service = DeployService(vercel=None, supabase=supabase)
    return deploy_service.get_deployments(idea_id)
