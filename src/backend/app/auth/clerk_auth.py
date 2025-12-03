# src/backend/app/auth/clerk_auth.py
import time
import requests
from jose import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from ..config import CLOUDFRONT  # placeholder if you used; not needed
from ..config import CLERK_ISSUER  # add to config
# from ..config import CLERK_AUD     # add to config

# Simple bearer
bearer = HTTPBearer(auto_error=False)

# Simple JWKS cache
_jwks_cache = {"keys": None, "fetched_at": 0}

def _fetch_jwks(issuer: str):
    now = time.time()
    if _jwks_cache["keys"] and now - _jwks_cache["fetched_at"] < 3600:
        return _jwks_cache["keys"]
    jwks_uri = issuer.rstrip("/") + "/.well-known/jwks.json"
    r = requests.get(jwks_uri, timeout=5)
    r.raise_for_status()
    jwks = r.json()
    _jwks_cache["keys"] = jwks
    _jwks_cache["fetched_at"] = now
    return jwks

def verify_clerk_admin_token(creds: HTTPAuthorizationCredentials = Depends(bearer)):
    """
    FastAPI dependency. Expects Authorization: Bearer <token>
    Verifies JWT signature via Clerk JWKS and checks admin role in public_metadata.role
    """
    if not creds:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    token = creds.credentials
    # get issuer from config
    issuer = CLERK_ISSUER
    if not issuer:
        raise HTTPException(status_code=500, detail="CLERK_ISSUER not configured")

    jwks = _fetch_jwks(issuer)
    try:
        # allow audience check if CLERK_AUD present; otherwise skip
        options = {"verify_aud": True} if CLERK_AUD else {"verify_aud": False}
        payload = jwt.decode(token, jwks, options=options, audience=CLERK_AUD)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

    # Clerk places public metadata in "public_metadata" claim in Clerk tokens
    public_md = payload.get("public_metadata", {}) or {}
    role = public_md.get("role") or public_md.get("userRole") or payload.get("role")
    # require role == 'admin'
    if role != "admin":
        raise HTTPException(status_code=403, detail="Not an admin")

    # return full payload for downstream use if needed
    return payload
