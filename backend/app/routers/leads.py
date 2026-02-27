from fastapi import APIRouter, Depends

from app.dependencies import get_supabase
from app.schemas.lead import LeadCreate, LeadResponse
from app.services.lead_service import LeadService

router = APIRouter()


@router.post("/leads", response_model=LeadResponse)
def capture_lead(
    body: LeadCreate,
    supabase=Depends(get_supabase),
):
    """Capture a lead from a landing page email form. Public endpoint."""
    service = LeadService(supabase)
    return service.save_lead(body)


@router.get("/ideas/{idea_id}/leads", response_model=list[LeadResponse])
def list_leads(
    idea_id: str,
    supabase=Depends(get_supabase),
):
    """List all leads captured for an idea."""
    service = LeadService(supabase)
    return service.get_leads(idea_id)
