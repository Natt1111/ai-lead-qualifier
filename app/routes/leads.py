import anthropic
from fastapi import APIRouter, HTTPException
from app.models import LeadSubmission, QualificationResult
from app.ai_qualifier import qualify_lead
from app.airtable_client import save_lead

router = APIRouter()


@router.post("", response_model=QualificationResult, status_code=201)
async def submit_lead(lead: LeadSubmission):
    # Step 1 — AI qualification
    try:
        result = await qualify_lead(lead)
    except anthropic.AuthenticationError:
        raise HTTPException(status_code=500, detail="Invalid Anthropic API key.")
    except anthropic.RateLimitError:
        raise HTTPException(status_code=429, detail="Claude API rate limit reached. Try again shortly.")
    except anthropic.APIConnectionError:
        raise HTTPException(status_code=502, detail="Could not reach Claude API. Check your network.")
    except anthropic.APIError as exc:
        raise HTTPException(status_code=502, detail=f"Claude API error: {exc.message}")

    # Step 2 — persist to Airtable
    try:
        await save_lead(lead, result)
    except Exception as exc:
        # Airtable failure should not block the caller from receiving the AI result.
        # Log the error but still return the qualification so the frontend stays responsive.
        print(f"[airtable] save_lead failed: {exc}")

    return result
