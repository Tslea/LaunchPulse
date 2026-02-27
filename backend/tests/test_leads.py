from unittest.mock import MagicMock


def test_capture_lead(client, mock_supabase):
    """POST /api/v1/leads should save a lead from landing page."""
    mock_supabase.table.return_value.insert.return_value.execute.return_value = MagicMock(
        data=[
            {
                "id": "lead-uuid-1",
                "email": "test@example.com",
                "idea_id": "idea-uuid-1",
                "utm_source": "tiktok",
                "utm_medium": "cpc",
                "utm_campaign": "validation_test",
                "referrer": "",
                "variant": "A",
                "created_at": "2026-02-27T10:00:00Z",
            }
        ]
    )

    response = client.post(
        "/api/v1/leads",
        json={
            "email": "test@example.com",
            "idea_id": "idea-uuid-1",
            "utm_source": "tiktok",
            "utm_medium": "cpc",
            "utm_campaign": "validation_test",
            "variant": "A",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["idea_id"] == "idea-uuid-1"
    assert data["utm_source"] == "tiktok"


def test_capture_lead_invalid_email(client):
    """POST /api/v1/leads should reject invalid email addresses."""
    response = client.post(
        "/api/v1/leads",
        json={
            "email": "not-an-email",
            "idea_id": "idea-uuid-1",
        },
    )
    assert response.status_code == 422


def test_list_leads(client, mock_supabase):
    """GET /api/v1/ideas/{id}/leads should return leads for that idea."""
    mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = MagicMock(
        data=[
            {
                "id": "lead-1",
                "email": "a@example.com",
                "idea_id": "idea-1",
                "utm_source": "",
                "utm_medium": "",
                "utm_campaign": "",
                "referrer": "",
                "variant": "A",
                "created_at": "2026-02-27T10:00:00Z",
            },
            {
                "id": "lead-2",
                "email": "b@example.com",
                "idea_id": "idea-1",
                "utm_source": "tiktok",
                "utm_medium": "",
                "utm_campaign": "",
                "referrer": "",
                "variant": "B",
                "created_at": "2026-02-27T11:00:00Z",
            },
        ]
    )

    response = client.get("/api/v1/ideas/idea-1/leads")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
