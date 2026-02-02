"""
Security: Telegram Login Widget validation and JWT (create/decode).
"""

from datetime import datetime, timezone, timedelta
from typing import Any
from jose import JWTError, jwt

from app.core.config import settings
from app.core.telegram_auth import validate_telegram_login_hash


def validate_telegram_hash(payload: dict[str, Any], bot_token: str) -> bool:
    """
    Verify Telegram Login Widget data integrity using BOT_TOKEN.
    Uses HMAC-SHA256 check of the `hash` field.
    """
    return validate_telegram_login_hash(payload, bot_token)


def create_access_token(user_id: str) -> str:
    """Issue a JWT access token for the given user id (sub claim)."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode = {
        "sub": user_id,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm="HS256",
    )


def decode_access_token(token: str) -> str | None:
    """
    Decode JWT and return user_id (sub) if valid and not expired.
    Returns None if invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=["HS256"],
        )
        sub = payload.get("sub")
        if sub is None:
            return None
        return str(sub)
    except JWTError:
        return None
