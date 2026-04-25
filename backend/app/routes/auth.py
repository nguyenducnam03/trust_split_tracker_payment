from fastapi import APIRouter, HTTPException, Security
from bson import ObjectId
from app.models.user import RegisterRequest, LoginRequest, TokenResponse, RefreshRequest, UserOut
from app.services.auth import hash_password, verify_password, create_access_token, create_refresh_token, decode_token, get_current_user_id
from app.services.database import get_db
from datetime import datetime, timezone

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=TokenResponse)
async def register(body: RegisterRequest):
    db = get_db()
    existing = await db.users.find_one({"email": body.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    result = await db.users.insert_one({
        "email": body.email,
        "password_hash": hash_password(body.password),
        "name": body.name,
        "created_at": datetime.now(timezone.utc),
    })

    user_id = str(result.inserted_id)
    return TokenResponse(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id),
    )

@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest):
    db = get_db()
    user = await db.users.find_one({"email": body.email.lower().strip()})
    if not user or not verify_password(body.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user_id = str(user["_id"])
    return TokenResponse(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id),
    )

@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: RefreshRequest):
    user_id = decode_token(body.refresh_token, "refresh")
    return TokenResponse(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id),
    )

@router.get("/me", response_model=UserOut)
async def me(user_id: str = Security(get_current_user_id)):
    db = get_db()
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(id=str(user["_id"]), email=user["email"], name=user["name"])
