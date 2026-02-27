def test_generate_prd_for_idea(client, mock_claude, mock_supabase, sample_idea_card, sample_prd):
    """POST /api/v1/ideas/{id}/generate-prd should generate and store a PRD."""
    # Mock get_idea
    mock_supabase.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value = type(
        "Result", (), {"data": {
            "id": "idea-1",
            "idea_card": sample_idea_card.model_dump(),
            "status": "draft",
            "created_at": "2026-02-27T10:00:00Z",
            "updated_at": "2026-02-27T10:00:00Z",
        }}
    )()

    # Mock Claude PRD generation
    mock_claude.generate_structured.return_value = (sample_prd, 800)

    # Mock Supabase upsert for PRD
    mock_supabase.table.return_value.upsert.return_value.execute.return_value = type(
        "Result", (), {"data": [{"id": "prd-1"}]}
    )()

    response = client.post("/api/v1/ideas/idea-1/generate-prd")
    assert response.status_code == 200
    data = response.json()
    assert "executive_summary" in data
    assert "landing_brief" in data
    assert "ads_brief" in data
