"""
Sofia Core Governance System v1.0.0

Institutional-grade governance, compliance, and audit system for Sofia Core.
Provides hash-chained audit logs, FRE Rule 902(13) compliance, expert witness
mode, multi-jurisdiction policy support, and court-ready exhibit generation.
"""

from .audit import AuditLogger, AuditEntry, ChainVerificationResult
from .policy import PolicyEngine, Policy, PolicyViolation

__all__ = [
    "AuditLogger",
    "AuditEntry", 
    "ChainVerificationResult",
    "PolicyEngine",
    "Policy",
    "PolicyViolation",
]

__version__ = "1.0.0"
