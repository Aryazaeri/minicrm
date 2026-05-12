import json
import google.generativeai as genai
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.lead import Lead
from app.models.user import User

router = APIRouter(prefix="/api/ai", tags=["ai"])

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

MODEL = "gemini-2.5-flash"


class NextActionResponse(BaseModel):
    suggestion: str


class ExtractRequest(BaseModel):
    text: str


class ExtractedEntities(BaseModel):
    people: list[str] = []
    dates: list[str] = []
    amounts: list[str] = []
    companies: list[str] = []


def _require_api_key():
    if not settings.GEMINI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="AI features unavailable: GEMINI_API_KEY not configured",
        )


@router.post("/leads/{lead_id}/suggest-next-action", response_model=NextActionResponse)
def suggest_next_action(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _require_api_key()
    lead = db.query(Lead).filter(Lead.id == lead_id, Lead.owner_id == current_user.id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    prompt = f"""You are a sales coach. Given this CRM lead, suggest ONE concrete next action the sales rep should take. Be specific and actionable. Limit to 2 sentences.

Lead title: {lead.title}
Stage: {lead.stage.value}
Value: ${lead.value:,.0f}
Notes: {lead.notes or "(no notes)"}

Respond with just the suggestion, no preamble."""

    try:
        model = genai.GenerativeModel(MODEL)
        result = model.generate_content(prompt)
        return NextActionResponse(suggestion=result.text.strip())
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI request failed: {e}")


@router.post("/extract-entities", response_model=ExtractedEntities)
def extract_entities(
    payload: ExtractRequest,
    current_user: User = Depends(get_current_user),
):
    _require_api_key()
    if not payload.text.strip():
        return ExtractedEntities()

    prompt = f"""Extract entities from this sales note. Return STRICT JSON only, no markdown fences. Schema:
{{"people": [...], "dates": [...], "amounts": [...], "companies": [...]}}

Note:
{payload.text}"""

    try:
        model = genai.GenerativeModel(
            MODEL,
            generation_config={"response_mime_type": "application/json"},
        )
        result = model.generate_content(prompt)
        data = json.loads(result.text)
        return ExtractedEntities(**data)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI request failed: {e}")
