import pytest

from app.templates.engine import render_template


def test_render_simple_placeholders(sample_landing_content):
    """Template engine should replace simple {{placeholder}} values."""
    values = sample_landing_content.model_dump()
    config = {
        "idea_id": "test-123",
        "api_base_url": "http://localhost:8000",
        "tiktok_pixel_id": "",
    }
    html = render_template("landing_v1.html", values, config)

    assert "Stop losing customers with ignored emails" in html
    assert "Start Free Now" in html
    assert "MailPilot" in html
    assert "No credit card required" in html


def test_render_array_sections(sample_landing_content):
    """Template engine should render repeated sections for arrays."""
    values = sample_landing_content.model_dump()
    config = {"idea_id": "test-123", "api_base_url": "", "tiktok_pixel_id": ""}
    html = render_template("landing_v1.html", values, config)

    # Problem bullets
    assert "Hours wasted writing emails" in html
    assert "Declining open rates" in html

    # Benefits
    assert "Save 10+ Hours/Week" in html
    assert "2x Your Open Rates" in html

    # Steps
    assert "Describe your campaign" in html
    assert "AI creates &amp; optimizes" in html

    # Testimonials
    assert "Marco Rossi" in html
    assert "Sara Chen" in html

    # FAQ
    assert "What is MailPilot?" in html
    assert "How much does it cost?" in html


def test_render_html_escaping(sample_landing_content):
    """Template engine should HTML-escape values to prevent XSS."""
    values = sample_landing_content.model_dump()
    values["headline"] = '<script>alert("xss")</script>'
    config = {"idea_id": "test-123", "api_base_url": "", "tiktok_pixel_id": ""}
    html = render_template("landing_v1.html", values, config)

    assert "<script>alert" not in html
    assert "&lt;script&gt;" in html


def test_render_output_size(sample_landing_content):
    """Rendered HTML should be under 80KB."""
    values = sample_landing_content.model_dump()
    config = {"idea_id": "test-123", "api_base_url": "", "tiktok_pixel_id": ""}
    html = render_template("landing_v1.html", values, config)

    size_bytes = len(html.encode("utf-8"))
    assert size_bytes < 80_000, f"HTML is {size_bytes} bytes, expected < 80KB"


def test_render_contains_required_meta(sample_landing_content):
    """Rendered HTML should contain required meta tags and structure."""
    values = sample_landing_content.model_dump()
    config = {"idea_id": "test-123", "api_base_url": "", "tiktok_pixel_id": ""}
    html = render_template("landing_v1.html", values, config)

    assert '<meta name="viewport"' in html
    assert '<meta name="description"' in html
    assert 'og:title' in html
    assert 'og:description' in html
    assert 'twitter:card' in html
    assert 'FAQPage' in html
    assert '<form' in html
    assert 'type="email"' in html


def test_render_config_injection(sample_landing_content):
    """Config values should be injected into the template."""
    values = sample_landing_content.model_dump()
    config = {
        "idea_id": "my-idea-uuid",
        "api_base_url": "https://api.launchpulse.app",
        "tiktok_pixel_id": "PIXEL123",
    }
    html = render_template("landing_v1.html", values, config)

    assert "my-idea-uuid" in html
    assert "https://api.launchpulse.app" in html
    assert "PIXEL123" in html
