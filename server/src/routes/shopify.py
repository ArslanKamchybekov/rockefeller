from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
import os
import hmac
import hashlib
import httpx
from urllib.parse import urlencode
import dotenv

router = APIRouter(prefix="", tags=["shopify"])

dotenv.load_dotenv()

def get_env(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise HTTPException(status_code=500, detail=f"Missing env var: {name}")
    return val



def verify_hmac(query_params: dict) -> bool:
    """Verify HMAC according to Shopify OAuth spec."""
    shared_secret = get_env("SHOPIFY_API_SECRET")
    hmac_param = query_params.get("hmac")
    if not hmac_param:
        return False

    # Build message by removing hmac and signature, sort lexicographically
    message_params = {k: v for k, v in query_params.items() if k not in ["hmac", "signature"]}
    sorted_params = sorted([f"{k}={v}" for k, v in message_params.items()])
    message = "&".join(sorted_params)

    digest = hmac.new(shared_secret.encode(), message.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, hmac_param)


@router.get("/auth")
async def shopify_oauth_start(shop: str, host: str | None = None):
    """Redirect merchant to Shopify OAuth install screen."""
    # Clean shop parameter - remove https:// if present
    if shop.startswith("https://"):
        shop = shop.replace("https://", "")
    if shop.startswith("http://"):
        shop = shop.replace("http://", "")
    
    api_key = get_env("SHOPIFY_API_KEY")
    scopes = os.getenv("SHOPIFY_SCOPES", "read_products,write_products,read_themes,write_themes,read_orders,read_customers")
    app_url = os.getenv("APP_URL", "http://localhost:8000")
    redirect_uri = f"{app_url}/auth/callback"

    params = {
        "client_id": api_key,
        "scope": scopes,
        "redirect_uri": redirect_uri,
        "state": "nonce-123",  # optionally generate per-request
    }
    return RedirectResponse(url=f"https://{shop}/admin/oauth/authorize?{urlencode(params)}", status_code=302)


@router.get("/auth/callback")
async def shopify_oauth_callback(request: Request, shop: str, code: str, state: str | None = None, hmac: str | None = None):
    """Exchange code for a permanent access token."""
    print(f"OAuth callback received: shop={shop}, code={code[:10]}..., hmac={hmac}")
    
    # HMAC verification (best-effort). If you prefer, enforce it strictly.
    if not verify_hmac(dict(request.query_params)):
        print("HMAC verification failed")
        raise HTTPException(status_code=400, detail="Invalid HMAC signature")

    api_key = get_env("SHOPIFY_API_KEY")
    api_secret = get_env("SHOPIFY_API_SECRET")
    async with httpx.AsyncClient(timeout=30.0) as client:
        token_resp = await client.post(
            f"https://{shop}/admin/oauth/access_token",
            json={
                "client_id": api_key,
                "client_secret": api_secret,
                "code": code,
            },
        )
        token_resp.raise_for_status()
        token_data = token_resp.json()
        access_token = token_data.get("access_token")
        if not access_token:
            print("No access token received from Shopify")
            raise HTTPException(status_code=400, detail="No access_token returned by Shopify")

        # Get scopes from the token response
        scopes = token_data.get("scope", "").split(",") if token_data.get("scope") else []
        
        # Encode the token data to pass to frontend
        import json
        import base64
        token_data_encoded = base64.b64encode(json.dumps({
            'access_token': access_token,
            'scopes': scopes,
            'shop': shop,
            'metadata': {
                'shop_name': shop,
                'api_version': '2024-10'
            }
        }).encode()).decode()

    # Redirect back to frontend with token data
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    redirect_url = f"{frontend_url}/integrations?shopify_installed=1&shop={shop}&token_data={token_data_encoded}"
    print(f"Redirecting to: {redirect_url}")
    return RedirectResponse(url=redirect_url, status_code=302)


