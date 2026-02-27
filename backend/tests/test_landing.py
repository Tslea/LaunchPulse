from unittest.mock import MagicMock


def test_generate_landing_page_requires_prd(client, mock_claude, mock_supabase):
    """POST /api/v1/ideas/{id}/landing-page should fail if PRD doesn't exist."""
    # Mock PRD not found
    mock_supabase.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value = MagicMock(
        data=None
    )

    response = client.post("/api/v1/ideas/test-uuid/landing-page")
    assert response.status_code == 400
    assert "PRD not found" in response.json()["detail"]


def test_preview_landing_page_not_found(client, mock_supabase):
    """GET /api/v1/ideas/{id}/landing-page/preview should 404 if not generated."""
    mock_supabase.table.return_value.select.return_value.eq.return_value.eq.return_value.single.return_value.execute.return_value = MagicMock(
        data=None
    )

    response = client.get("/api/v1/ideas/test-uuid/landing-page/preview")
    assert response.status_code == 404
