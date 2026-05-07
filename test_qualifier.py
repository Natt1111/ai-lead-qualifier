"""Quick smoke test — run with: python test_qualifier.py"""

import asyncio
from app.models import LeadSubmission
from app.ai_qualifier import qualify_lead


HOT_LEAD = LeadSubmission(
    name="Sarah Chen",
    email="schen@fintech-corp.com",
    company="FinTech Corp",
    role="VP of Sales",
    use_case=(
        "We need to automate lead qualification for our SDR team immediately. "
        "We're closing our Q3 budget cycle and need a solution deployed within 30 days. "
        "Currently losing deals because reps spend too much time on unqualified prospects."
    ),
    budget="$5,000 – $20,000/mo",
    timeline="Immediately",
)


async def main() -> None:
    print("Qualifying sample lead...\n")
    result = await qualify_lead(HOT_LEAD)

    print(f"Score:       {result.lead_score}/100")
    print(f"Tier:        {result.score.value}")
    print(f"\nSummary:\n{result.summary}")
    print(f"\nEmail draft:\n{result.email_draft}")


if __name__ == "__main__":
    asyncio.run(main())
