from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import os
import hmac
import hashlib
import base64
import httpx
from urllib.parse import urlencode

# Load environment variables if .env present
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

app = FastAPI(title="Rockefeller API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .routes.shopify import router as shopify_router

app.include_router(shopify_router)

@app.get("/")
async def root():
    return {"message": "Hello from Rockefeller API!", "shopify": "/auth, /auth/callback, /api/*, /api/webhooks"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/docs_search", response_model=LegalDocsOutput)
async def docs_test(body: LegalDocsInput) -> LegalDocsOutput:
    response: LegalDocsOutput = generate_legal_docs({ "idea": body.idea })
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
