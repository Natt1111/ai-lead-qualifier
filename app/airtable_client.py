import asyncio
from pyairtable import Api
from app.config import settings
from app.models import LeadSubmission, QualificationResult


def _get_table():
    api = Api(settings.AIRTABLE_TOKEN)
    return api.table(settings.AIRTABLE_BASE_ID, settings.AIRTABLE_TABLE_NAME)


def _build_fields(lead: LeadSubmission, result: QualificationResult) -> dict:
    """Map model fields to Airtable column names. Column names must match the table exactly."""
    fields = {
        "Name": lead.name,
        "Email": lead.email,
        "Company": lead.company,
        "Message": lead.message,
        "Status": "New",
    }
    if lead.phone:
        fields["Phone"] = lead.phone
    return fields


def _sync_save(lead: LeadSubmission, result: QualificationResult) -> str:
    record = _get_table().create(_build_fields(lead, result))
    return record["id"]


def _sync_get(record_id: str) -> dict:
    return _get_table().get(record_id)


def _sync_list(max_records: int) -> list[dict]:
    return _get_table().all(max_records=max_records)


# pyairtable is synchronous — run blocking calls in a thread pool so the
# FastAPI event loop is never blocked.

async def save_lead(lead: LeadSubmission, result: QualificationResult) -> str:
    """Create a new Airtable record and return its record ID."""
    return await asyncio.to_thread(_sync_save, lead, result)


async def get_lead(record_id: str) -> dict:
    """Fetch a single Airtable record by ID."""
    return await asyncio.to_thread(_sync_get, record_id)


async def list_leads(max_records: int = 100) -> list[dict]:
    """Return up to max_records leads from Airtable."""
    return await asyncio.to_thread(_sync_list, max_records)
