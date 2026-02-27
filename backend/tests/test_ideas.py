from unittest.mock import MagicMock

from app.schemas.idea import IdeaCard


def test_create_idea(client, mock_claude, mock_supabase, sample_idea_card):
    """POST /api/v1/ideas should structure idea via Claude and store in Supabase."""
    # Mock Claude to return a structured IdeaCard
    mock_claude.generate_structured.return_value = (sample_idea_card, 150)

    # Mock Supabase insert
    mock_supabase.table.return_value.insert.return_value.execute.return_value = MagicMock(
        data=[
            {
                "id": "test-uuid-123",
                "idea_card": sample_idea_card.model_dump(),
                "status": "draft",
                "created_at": "2026-02-27T10:00:00Z",
                "updated_at": "2026-02-27T10:00:00Z",
            }
        ]
    )

    response = client.post(
        "/api/v1/ideas",
        json={
            "description": "An AI tool that writes and optimizes email campaigns automatically for small businesses",
            "target_audience": "Solo founders and small business owners",
            "problem": "Email marketing takes too long and results are declining",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "test-uuid-123"
    assert data["idea_card"]["name"] == "MailPilot"
    assert data["status"] == "draft"
    mock_claude.generate_structured.assert_called_once()


def test_list_ideas(client, mock_supabase, sample_idea_card):
    """GET /api/v1/ideas should return all ideas."""
    mock_supabase.table.return_value.select.return_value.order.return_value.execute.return_value = MagicMock(
        data=[
            {
                "id": "test-uuid-123",
                "idea_card": sample_idea_card.model_dump(),
                "status": "draft",
                "created_at": "2026-02-27T10:00:00Z",
                "updated_at": "2026-02-27T10:00:00Z",
            }
        ]
    )

    response = client.get("/api/v1/ideas")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["idea_card"]["name"] == "MailPilot"


def test_get_idea(client, mock_supabase, sample_idea_card):
    """GET /api/v1/ideas/{id} should return a single idea."""
    mock_supabase.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value = MagicMock(
        data={
            "id": "test-uuid-123",
            "idea_card": sample_idea_card.model_dump(),
            "status": "live",
            "created_at": "2026-02-27T10:00:00Z",
            "updated_at": "2026-02-27T10:00:00Z",
        }
    )

    response = client.get("/api/v1/ideas/test-uuid-123")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "test-uuid-123"
    assert data["status"] == "live"
