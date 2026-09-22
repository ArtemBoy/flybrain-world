from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class SensoryState:
    bearing: float
    distance: float

class BrainController(ABC):
    @abstractmethod
    def act(self, sensory: SensoryState) -> str:
        """Return LEFT, FORWARD, or RIGHT."""
        raise NotImplementedError
