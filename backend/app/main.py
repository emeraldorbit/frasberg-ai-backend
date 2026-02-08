"""Sofia Core v4.0.0 - Distributed Sovereign Intelligence with Quantum-Ready Architecture."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from voice import voice_router
from governance import governance_router
from ai import ai_router
from memory import memory_router
from distributed import distributed_router
from quantum import quantum_router
from multimodal import multimodal_router

app = FastAPI(
    title="Sofia Core v4.0.0",
    description="Distributed Sovereign Intelligence with Quantum-Ready Architecture",
    version="4.0.0"
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
app.include_router(distributed_router)
app.include_router(quantum_router)
app.include_router(multimodal_router)

@app.get("/")
async def root():
    return {
        "name": "Sofia Core",
        "type": "Distributed Sovereign Intelligence with Quantum-Ready Architecture",
        "version": "4.0.0",
        "status": "operational",
        "revolutionary_features_v4": [
            "Distributed Mesh Architecture (P2P multi-node)",
            "Quantum-Ready Cryptography (CRYSTALS-Kyber, Dilithium)",
            "Zero-Knowledge Proofs (ZK-SNARKs)",
            "Blockchain-based Consensus",
            "Multi-Modal AI Fusion (vision + voice + text)",
            "Finance Fork (port 8005) - Compliance & fraud detection",
            "Government Fork (port 8006) - Public service & policy",
            "Medical Research Fork (port 8007) - Non-clinical research",
            "Service Discovery & Auto-Scaling",
            "Self-Healing Infrastructure (foundation)"
        ],
        "maintained_from_v3": [
            "AI Orchestration (5 LLM providers)",
            "Hallucination detection",
            "Transparent reasoning chains",
            "Long-term memory system",
            "Legal Fork (8003)",
            "Research Fork (8004)"
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
        "version": "4.0.0"
    }

@app.get("/api/v4/system/info")
async def system_info():
    return {
        "version": "4.0.0",
        "architecture": "Distributed quantum-ready sovereign intelligence",
        "services": 10,  # Canonical + Education + Healthcare + Legal + Research + Finance + Government + Med Research + Analytics + Frontend
        "capabilities": {
            "distributed": {
                "mesh_networking": True,
                "p2p_coordination": True,
                "blockchain_consensus": True,
                "service_discovery": True,
                "zero_downtime_failover": True,
                "geographic_distribution": True
            },
            "quantum": {
                "post_quantum_encryption": True,
                "algorithms": ["CRYSTALS-Kyber", "NTRU"],
                "quantum_safe_signatures": True,
                "signature_algorithms": ["CRYSTALS-Dilithium", "FALCON"],
                "zero_knowledge_proofs": True,
                "zkp_types": ["ZK-SNARKs", "ZK-STARKs", "Bulletproofs"],
                "future_proof": True
            },
            "ai": {
                "llm_providers": 5,
                "multimodal": True,
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
                "privacy_safe": True,
                "distributed": True
            },
            "forks": 7  # Education, Healthcare, Legal, Research, Finance, Government, Medical Research
        }
    }
