from datetime import datetime

from pydantic import BaseModel, Field


class DeployRequest(BaseModel):
    idea_id: str
    variant: str = Field(default="A", description="A/B variant identifier")


class DeployResponse(BaseModel):
    id: str
    idea_id: str
    url: str = Field(description="Live deployment URL")
    variant: str
    created_at: datetime | None = None
