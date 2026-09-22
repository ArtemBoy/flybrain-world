from __future__ import annotations

from brain.base import BrainController, SensoryState

class ToyBrain(BrainController):
    """Smoke-test controller only. This is NOT a biological fly-brain model."""
    def __init__(self, turn_threshold: float = 0.18) -> None:
        self.turn_threshold = turn_threshold

    def act(self, sensory: SensoryState) -> str:
        if sensory.bearing < -self.turn_threshold:
            return "LEFT"
        if sensory.bearing > self.turn_threshold:
            return "RIGHT"
        return "FORWARD"
