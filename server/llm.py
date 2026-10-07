from typing import List
from .models import Issue, TestSuggestion

def enrich_with_llm(issues: List[Issue], path_to_source: dict) -> List[TestSuggestion]:
    """
    Placeholder: add simple explanations/suggestions without external LLM.
    Later we will replace with a real LLM call.
    """
    tests: List[TestSuggestion] = []
    for i in issues:
        if not i.explanation:
            i.explanation = "Automated static analysis flagged this pattern; review and fix if applicable."
        if not i.suggestion:
            if i.ruleId == "PY.AST.MUTABLE_DEFAULT":
                i.suggestion = "Use None as default and initialize inside the function."
            elif i.ruleId == "PY.AST.BROAD_EXCEPT":
                i.suggestion = "Catch specific exception types and handle separately."
            elif i.ruleId.startswith("PY.AST.UNUSED_"):
                i.suggestion = "Remove the unused symbol, or prefix with '_' if intentional."
            else:
                i.suggestion = "Refactor or add guards to improve safety/performance."
        # naive test scaffold if we find a top-level 'def' in the file
        # (real LLM would tailor this)
    return tests
