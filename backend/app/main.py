"""Sofia Core v3.0.0 - Main FastAPI Application with AI Orchestration."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from voice import voice_router
from governance import governance_router
from ai import ai_router
from memory import memory_router

app = FastAPI(
    title="Sofia Core v3.0.0",
    description="Autonomous Institution-Grade Operational Intelligence",
    version="3.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(voice_router)
app.include_router(governance_router)
app.include_router(ai_router)
app.include_router(memory_router)

@app.get("/")
async def root():
    return {
        "name": "Sofia Core",
        "type": "Autonomous Institution-Grade Operational Intelligence",
        "version": "3.0.0",
        "status": "operational",
        "new_features_v3": [
            "AI Orchestration Layer (5 LLM providers)",
            "Hallucination detection & validation",
            "Transparent reasoning chains",
            "Long-term memory system",
            "Context management",
            "Legal Fork (port 8003)",
            "Research Fork (port 8004)",
            "Prompt engineering framework"
        ],
        "maintained_from_v2": [
            "Voice system (11 languages)",
            "Hash-chained audit logging",
            "FRE Rule 902 compliance",
            "Expert witness mode"
        ],
        "limitations": [
            "no intent",
            "no discretion",
            "no legal conclusions",
            "no medical diagnosis",
            "no biometric identification",
            "voice fingerprints are audit-only (not identification)",
            "AI responses validated against scope limits"
        ]
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "canonical-core",
        "version": "3.0.0"
    }

@app.get("/api/v3/system/info")
async def system_info():
    return {
        "version": "3.0.0",
        "architecture": "45-layer sovereign + AI orchestration + memory",
        "services": 7,  # Canonical + Education + Healthcare + Analytics + Frontend + Legal + Research
        "capabilities": {
            "ai": {
                "llm_providers": 5,
                "orchestration": True,
                "hallucination_detection": True,
                "reasoning_chains": True,
                "explainable": True
            },
            "voice": {
                "languages": 11,
                "emotions": 6,
                "real_time": True,
                "fingerprinting": True
            },
            "governance": {
                "audit_logging": True,
                "hash_chained": True,
                "rule_902": True,
                "expert_witness": True
            },
            "memory": {
                "long_term": True,
                "context_management": True,
                "privacy_safe": True
            },
            "forks": 4  # Education, Healthcare, Legal, Research
        }
    }
