import anthropic
from app.config import settings
from app.models import LeadSubmission, QualificationResult, LeadScore

SYSTEM_PROMPT = """You are an expert B2B sales qualification specialist. Analyze inbound leads \
and determine their quality based on buying intent, authority, budget signals, and timeline urgency.

Scoring criteria:
- Hot (score 70-100): Clear buying intent, decision-maker or strong influencer, explicit or \
implied budget, urgent timeline (immediately or 1-3 months), specific and well-defined use case.
- Warm (score 35-69): Interested but still exploring, may not be the final decision-maker, \
vague or no budget, longer timeline (3-6+ months), understood use case but no urgency.
- Cold (score 0-34): Vague inquiry, unclear need, no timeline, unlikely to be a buyer, \
or appears to be a student/researcher rather than a purchasing contact.

Write the follow-up email in first person as a sales representative. Keep it warm, professional, \
and personalized to their specific message with a clear call to action."""

_QUALIFICATION_TOOL: anthropic.types.ToolParam = {
    "name": "submit_qualification",
    "description": "Record the lead qualification result after analysis.",
    "input_schema": {
        "type": "object",
        "properties": {
            "lead_score": {
                "type": "integer",
                "description": "Numeric quality score 0-100.",
                "minimum": 0,
                "maximum": 100,
            },
            "qualification": {
                "type": "string",
                "enum": ["Hot", "Warm", "Cold"],
                "description": "Lead qualification tier.",
            },
            "summary": {
                "type": "string",
                "description": "2-3 sentence analysis of lead quality and reasoning.",
            },
            "email_draft": {
                "type": "string",
                "description": "Personalized follow-up email to send to the lead.",
            },
        },
        "required": ["lead_score", "qualification", "summary", "email_draft"],
    },
}


def _build_lead_context(lead: LeadSubmission) -> str:
    return (
        f"Lead Information:\n"
        f"- Name: {lead.name}\n"
        f"- Email: {lead.email}\n"
        f"- Phone: {lead.phone or 'Not provided'}\n"
        f"- Company: {lead.company}\n"
        f"- Message: {lead.message}"
    )


async def qualify_lead(lead: LeadSubmission) -> QualificationResult:
    """Call Claude with tool use to qualify a lead and return structured results."""

    client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    response = await client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        tools=[_QUALIFICATION_TOOL],
        tool_choice={"type": "tool", "name": "submit_qualification"},
        messages=[{"role": "user", "content": _build_lead_context(lead)}],
    )

    tool_block = next(b for b in response.content if b.type == "tool_use")
    data = tool_block.input

    return QualificationResult(
        lead_score=data["lead_score"],
        score=LeadScore(data["qualification"]),
        summary=data["summary"],
        email_draft=data["email_draft"],
    )
