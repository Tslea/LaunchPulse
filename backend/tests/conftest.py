from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.schemas.idea import IdeaCard
from app.schemas.landing import (
    FAQ,
    Benefit,
    LandingPageContent,
    SolutionFeature,
    Step,
    Testimonial,
)
from app.schemas.prd import AdsBrief, LandingBrief, PRDContent


@pytest.fixture
def mock_supabase():
    """Mocked Supabase client."""
    client = MagicMock()
    return client


@pytest.fixture
def mock_claude():
    """Mocked Claude client."""
    client = MagicMock()
    return client


@pytest.fixture
def mock_vercel():
    """Mocked Vercel client."""
    client = MagicMock()
    return client


@pytest.fixture
def app(mock_supabase, mock_claude, mock_vercel):
    """FastAPI test app with mocked dependencies."""
    from app.dependencies import get_claude_client, get_supabase, get_vercel_client
    from app.main import create_app

    test_app = create_app()
    test_app.dependency_overrides[get_supabase] = lambda: mock_supabase
    test_app.dependency_overrides[get_claude_client] = lambda: mock_claude
    test_app.dependency_overrides[get_vercel_client] = lambda: mock_vercel

    yield test_app

    test_app.dependency_overrides.clear()


@pytest.fixture
def client(app):
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def sample_idea_card() -> IdeaCard:
    return IdeaCard(
        name="MailPilot",
        one_liner="AI that writes and optimizes your email campaigns while you sleep",
        problem="Small businesses spend hours writing email campaigns that get ignored. Open rates are declining, and most founders don't have marketing expertise.",
        target_audience="Solo founders and small business owners (1-10 employees) who rely on email marketing but lack time and expertise to optimize it.",
        solution="An AI-powered email marketing assistant that generates, sends, and continuously optimizes email campaigns based on real engagement data.",
        unique_value="Set it and forget it — MailPilot learns from every send and improves automatically, unlike tools that just generate copy.",
        monetization="Freemium: free for up to 500 subscribers, $19/mo for up to 5000, $49/mo unlimited.",
        keywords=["email marketing", "AI email", "email automation", "marketing automation", "small business email"],
        tone="professional",
    )


@pytest.fixture
def sample_prd() -> PRDContent:
    return PRDContent(
        executive_summary="MailPilot is an AI-powered email marketing tool that automates campaign creation and optimization for small businesses.",
        problem_statement="Small businesses spend 5-10 hours per week on email marketing with declining returns. Open rates average 15-20% and most campaigns lack personalization.",
        target_audience_analysis="Solo founders and small business owners aged 25-45, tech-savvy but not marketing experts. Active on TikTok and Instagram.",
        proposed_solution="An AI assistant that generates email campaigns, A/B tests subject lines, optimizes send times, and learns from engagement patterns.",
        key_features=[
            "AI-generated email copy tailored to your brand voice",
            "Automatic A/B testing of subject lines and content",
            "Smart send-time optimization based on subscriber behavior",
            "One-click campaign setup from a brief description",
            "Real-time analytics dashboard with actionable insights",
        ],
        unique_value_proposition="The only email tool that gets smarter with every send — set up once, improve forever.",
        competitive_landscape="Mailchimp (complex, expensive), ConvertKit (creator-focused), Beehiiv (newsletter-focused). MailPilot is the first fully autonomous option.",
        success_metrics=["CTR > 2%", "Conversion rate > 3%", "CPL < €5", "100+ signups in 7 days"],
        monetization_strategy="Freemium model: free tier (500 subs), Pro at $19/mo (5000 subs), Business at $49/mo (unlimited).",
        landing_brief=LandingBrief(
            headline_suggestions=[
                "Stop losing customers with ignored emails",
                "Your emails, optimized by AI while you sleep",
            ],
            subheadline="The AI that writes, sends, and optimizes your email campaigns automatically",
            cta_text="Start Free",
            key_sections=["Hero", "Problem", "Solution", "Benefits", "Social Proof", "FAQ", "CTA"],
            messaging_angle="loss-aversion",
        ),
        ads_brief=AdsBrief(
            target_demographics="25-44, M/F, small business owners, marketers",
            interests=["entrepreneurship", "digital marketing", "email marketing", "small business"],
            suggested_daily_budget_eur=7.0,
            test_duration_days=5,
            creative_angles=["Pain point: wasted hours", "Social proof: results", "Demo: how easy it is"],
            tiktok_hashtags=["#emailmarketing", "#smallbusiness", "#aitool", "#marketingautomation"],
        ),
    )


@pytest.fixture
def sample_landing_content() -> LandingPageContent:
    return LandingPageContent(
        headline="Stop losing customers with ignored emails",
        subheadline="The AI that writes, sends, and optimizes your email campaigns while you sleep",
        cta_text="Start Free Now",
        cta_subtext="No credit card required",
        problem_title="The email problem you know too well",
        problem_description="You spend hours crafting the perfect email, hit send, and... crickets. Open rates keep dropping, and you don't have time to test what works.",
        problem_bullets=[
            "Hours wasted writing emails that nobody opens",
            "Declining open rates with no clear fix",
            "No time to A/B test and optimize campaigns",
        ],
        solution_title="Meet MailPilot: your AI email co-pilot",
        solution_description="MailPilot generates, sends, and optimizes your email campaigns automatically. Just describe what you want to say, and the AI handles everything else.",
        solution_features=[
            SolutionFeature(icon="🤖", text="AI writes personalized emails in your brand voice"),
            SolutionFeature(icon="📊", text="Automatic A/B testing finds what works best"),
            SolutionFeature(icon="⏰", text="Smart scheduling sends at the perfect time"),
        ],
        benefits=[
            Benefit(icon="⚡", title="Save 10+ Hours/Week", description="Stop writing emails manually. MailPilot generates and sends campaigns in minutes, not hours."),
            Benefit(icon="📈", title="2x Your Open Rates", description="AI-optimized subject lines and send times consistently outperform manual campaigns."),
            Benefit(icon="🎯", title="Set It & Forget It", description="Configure once, and MailPilot learns and improves with every campaign automatically."),
        ],
        testimonials=[
            Testimonial(name="Marco Rossi", role="Founder, TechFlow SaaS", quote="MailPilot increased our open rates from 18% to 42% in just 3 weeks. I save 8 hours every week."),
            Testimonial(name="Sara Chen", role="E-commerce Owner", quote="I went from dreading email campaigns to not even thinking about them. Revenue from email is up 67%."),
        ],
        steps=[
            Step(number=1, title="Describe your campaign", description="Tell MailPilot what you want to communicate in a few words."),
            Step(number=2, title="AI creates & optimizes", description="MailPilot generates copy, tests variants, and picks the best send time."),
            Step(number=3, title="Watch results roll in", description="Track opens, clicks, and conversions on your real-time dashboard."),
        ],
        faq=[
            FAQ(question="What is MailPilot?", answer="MailPilot is an AI-powered email marketing tool that automatically writes, sends, and optimizes your email campaigns."),
            FAQ(question="How much does it cost?", answer="MailPilot is free for up to 500 subscribers. Pro plans start at $19/month for up to 5,000 subscribers."),
            FAQ(question="Do I need marketing experience?", answer="Not at all. Just describe what you want to say, and MailPilot handles the rest — copywriting, testing, and optimization."),
            FAQ(question="Is my data safe?", answer="Yes. We use bank-level encryption and never share your subscriber data with third parties. Fully GDPR compliant."),
        ],
        urgency_text="First 100 users get lifetime access to the Pro plan",
        page_title="MailPilot — AI Email Marketing on Autopilot",
        meta_description="Stop wasting hours on email campaigns. MailPilot writes, sends, and optimizes your emails automatically. Free for up to 500 subscribers.",
        brand_name="MailPilot",
        brand_color="#E94560",
    )
