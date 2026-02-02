"""Telegram Login Widget hash validation (HMAC-SHA256)."""

import hashlib
import hmac
from typing import Any


def validate_telegram_login_hash(payload: dict[str, Any], bot_token: str) -> bool:
    """
    Verify the hash from Telegram Login Widget.
    - data_check_string = sorted key=value (excluding hash), newline-separated.
    - secret_key = SHA256(bot_token).
    - computed = HMAC-SHA256(secret_key, data_check_string).hexdigest().
    """
    if not bot_token or "hash" not in payload:
        return False
    received_hash = payload["hash"]
    # Build data-check-string: all fields except hash, sorted by key
    data_dict = {k: v for k, v in payload.items() if k != "hash" and v is not None}
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(data_dict.items()))
    # secret_key = SHA256(bot_token)
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    # HMAC-SHA256(secret_key, data_check_string)
    computed = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(computed, received_hash)
