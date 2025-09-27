from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agents.docs import generate_legal_docs
from models.docs import LegalDocsInput, LegalDocsOutput

app = FastAPI(title="Rockefeller API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello from Rockefeller API!"}

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
