from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class IdeaStatus(str, Enum):
    DRAFT = "draft"
    GENERATING = "generating"
    LIVE = "live"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class IdeaCreate(BaseModel):
    """Raw user input when creating a new idea."""

    description: str = Field(
        ..., min_length=10, max_length=2000, description="Free-text idea description (1-3 sentences)"
    )
    target_audience: str = Field(default="", description="Who is the target user?")
    problem: str = Field(default="", description="What problem does it solve?")
    differentiation: str = Field(default="", description="What makes it unique?")
    business_model: str = Field(default="", description="How will it make money?")


class IdeaCard(BaseModel):
    """Structured idea after AI processing — input for all downstream modules."""

    name: str = Field(..., description="Short product/idea name")
    one_liner: str = Field(..., description="One-sentence pitch")
    problem: str = Field(..., description="Problem statement (2-3 sentences)")
    target_audience: str = Field(..., description="Primary target audience description")
    solution: str = Field(..., description="Proposed solution (2-3 sentences)")
    unique_value: str = Field(..., description="Unique value proposition")
    monetization: str = Field(..., description="Revenue model")
    keywords: list[str] = Field(default_factory=list, description="SEO/targeting keywords")
    tone: str = Field(default="professional", description="Brand tone of voice")


class IdeaResponse(BaseModel):
    """Full idea record returned from API."""

    id: str
    idea_card: IdeaCard
    status: IdeaStatus = IdeaStatus.DRAFT
    created_at: datetime | None = None
    updated_at: datetime | None = None
