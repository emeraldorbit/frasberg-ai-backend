"""Sofia Core v1.0.0 - Main FastAPI Application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Sofia Core v1.0.0",
    description="Operational intelligence system - Automated, institutional-grade",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "name": "Sofia Core",
        "type": "Automated operational intelligence system",
        "version": "v1.0.0",
        "status": "operational",
        "limitations": [
            "no intent",
            "no discretion",
            "no legal conclusions",
            "no medical diagnosis",
            "no biometric identification"
        ]
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
