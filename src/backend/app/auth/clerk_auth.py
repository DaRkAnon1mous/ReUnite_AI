# src/backend/app/auth/clerk_auth.py
import time
import requests
import logging
from jose import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..config import CLERK_ISSUER, ADMIN_EMAIL

logger = logging.getLogger("clerk_auth")
bearer = HTTPBearer(auto_error=False)

_jwks_cache = {"keys": None, "fetched_at": 0}


def _fetch_jwks(issuer: str):
    now = time.time()
    if _jwks_cache["keys"] and now - _jwks_cache["fetched_at"] < 3600:
        return _jwks_cache["keys"]
    url = issuer.rstrip("/") + "/.well-known/jwks.json"
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    jwks = r.json()
    _jwks_cache["keys"] = jwks
    _jwks_cache["fetched_at"] = now
    return jwks


def verify_clerk_admin_token(creds: HTTPAuthorizationCredentials = Depends(bearer)):
    if not creds:
        raise HTTPException(401, "Missing authorization header")

    token = creds.credentials

    jwks = _fetch_jwks(CLERK_ISSUER)

    # Decode token using JWKS (python-jose supports passing JWKS dict)
    try:
        payload = jwt.decode(
            token,
            jwks,
            algorithms=["RS256"],
            options={"verify_aud": False},
            issuer=CLERK_ISSUER,
        )
    except Exception as e:
        logger.warning("Token decode failed: %s", e)
        raise HTTPException(401, f"Invalid token: {e}")

    # --- DEBUG LOGGING: show helpful parts of payload ---
    # IMPORTANT: this is only for debugging. Remove or lower log level in production.
    try:
        logger.info("Clerk token payload keys: %s", list(payload.keys()))
        # log likely useful fields
        logger.debug("token payload: %s", payload)
    except Exception:
        pass

    # Accept admin if either:
    #  - email matches ADMIN_EMAIL (various possible keys)
    #  - OR public_metadata.role == "admin"
    possible_emails = set()
    for k in ("email", "email_address", "primary_email_address"):
        v = payload.get(k)
        if v:
            possible_emails.add(v)

    if "email_addresses" in payload and isinstance(payload["email_addresses"], list):
        for item in payload["email_addresses"]:
            if isinstance(item, dict):
                e = item.get("email_address")
                if e:
                    possible_emails.add(e)

    # public_metadata often stored under "public_metadata" or "claims" depending on template
    public_md = payload.get("public_metadata") or payload.get("publicClaims") or {}
    role = None
    try:
        role = public_md.get("role") if isinstance(public_md, dict) else None
    except Exception:
        role = None

    # final check
    if ADMIN_EMAIL not in possible_emails and role != "admin":
        logger.info("Admin authorization failed. emails=%s role=%s", list(possible_emails), role)
        raise HTTPException(403, "Admin only")

    # success
    return payload
