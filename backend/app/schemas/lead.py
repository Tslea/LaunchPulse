from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class LeadCreate(BaseModel):
    """Lead captured from a landing page email form."""

    email: EmailStr
    idea_id: str
    utm_source: str = ""
    utm_medium: str = ""
    utm_campaign: str = ""
    referrer: str = ""
    variant: str = Field(default="A", description="A/B variant that captured this lead")


class LeadResponse(BaseModel):
    id: str
    email: str
    idea_id: str
    utm_source: str = ""
    utm_medium: str = ""
    utm_campaign: str = ""
    referrer: str = ""
    variant: str = "A"
    created_at: datetime | None = None
