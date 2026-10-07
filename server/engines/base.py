# server/engines/base.py
from typing import List, Tuple, Dict
from ..models import Issue

class EngineBase:
    language: str = "generic"
    extensions: Tuple[str, ...] = tuple()

    def analyze(self, path: str, source: str) -> Tuple[List[Issue], Dict[str, float]]:
        """
        Return (issues, metrics). Must be pure (no execution).
        metrics can include: {"functions": int, "complexity": float}
        """
        raise NotImplementedError()
