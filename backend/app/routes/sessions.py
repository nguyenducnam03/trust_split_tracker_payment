from fastapi import APIRouter, HTTPException, Security
from datetime import datetime, timezone
from bson import ObjectId
from app.models.session import CreateSessionRequest, ConfirmRequest, SessionOut
from app.services.database import get_db
from app.services.auth import get_current_user_id
from app.config import settings

router = APIRouter(prefix="/api/sessions", tags=["sessions"])

def serialize(doc) -> dict:
    doc["id"] = str(doc.pop("_id"))
    doc["share_url"] = f"{settings.frontend_url}/pay/{doc['id']}"
    return doc

@router.post("", response_model=SessionOut)
async def create_session(body: CreateSessionRequest, user_id: str = Security(get_current_user_id)):
    db = get_db()
    members = [{"name": m.name, "amount": m.amount, "confirmed": False, "confirmed_at": None} for m in body.members]
    doc = {
        "owner_id": user_id,
        "name": body.name,
        "cost_items": [c.model_dump() for c in body.cost_items],
        "members": members,
        "created_at": datetime.now(timezone.utc),
    }
    result = await db.sessions.insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize(doc)

@router.get("/{session_id}", response_model=SessionOut)
async def get_session(session_id: str):
    db = get_db()
    doc = await db.sessions.find_one({"_id": ObjectId(session_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Session not found")
    return serialize(doc)

@router.post("/{session_id}/confirm")
async def confirm_payment(session_id: str, body: ConfirmRequest):
    db = get_db()
    result = await db.sessions.update_one(
        {"_id": ObjectId(session_id), "members.name": body.member_name},
        {"$set": {"members.$.confirmed": True, "members.$.confirmed_at": datetime.now(timezone.utc)}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Session or member not found")
    return {"message": "Confirmed"}
