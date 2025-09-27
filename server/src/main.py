from fastapi import FastAPI, Request # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from pydantic import BaseModel
from urllib.parse import urlencode
from src.utils.email_agent_setup import email_setup
from src.agents.mail import respond_to_support_email

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

@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    email_setup()

@app.get("/")
async def root():
    return {"message": "Hello from Rockefeller API!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/email/webhook")
async def email_webhook(request: Request):
    body = await request.body()
    respond_to_support_email(body)
    return {"status": "received"}

if __name__ == "__main__":
    import uvicorn # type: ignore
    uvicorn.run(app, host="0.0.0.0", port=8000)
