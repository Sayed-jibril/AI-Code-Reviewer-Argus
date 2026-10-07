from pydantic import BaseModel
from typing import List, Literal, Optional

Severity = Literal["info", "warning", "error", "security"]

class Issue(BaseModel):
    id: str
    ruleId: str
    title: str
    severity: Severity
    filePath: str
    lineStart: int
    lineEnd: int
    codeFrame: Optional[str] = None
    explanation: Optional[str] = None
    suggestion: Optional[str] = None
    patchUnifiedDiff: Optional[str] = None
    tags: Optional[List[str]] = None
    confidence: float = 0.5

class TestSuggestion(BaseModel):
    filePath: str
    framework: Literal["pytest", "jest", "nunit"]
    rationale: str
    content: str

class ReviewMetrics(BaseModel):
    files: int
    functions: int
    avgComplexity: float
    estimatedBigO: Optional[str] = None

class ReviewResult(BaseModel):
    issues: List[Issue]
    tests: List[TestSuggestion]
    metrics: ReviewMetrics
