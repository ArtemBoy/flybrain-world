from __future__ import annotations

from dataclasses import dataclass
from math import atan2, cos, hypot, pi, sin
from brain.base import SensoryState

def wrap_angle(x: float) -> float:
    return (x + pi) % (2 * pi) - pi

@dataclass
class Agent:
    x: float = 0.0
    y: float = 0.0
    heading: float = 0.0

@dataclass(frozen=True)
class Target:
    x: float
    y: float

class Arena:
    def __init__(self, target: Target, step_size: float = 0.25, turn_size: float = 0.25) -> None:
        self.agent = Agent()
        self.target = target
        self.step_size = step_size
        self.turn_size = turn_size

    def sense(self) -> SensoryState:
        dx = self.target.x - self.agent.x
        dy = self.target.y - self.agent.y
        return SensoryState(wrap_angle(atan2(dy, dx) - self.agent.heading), hypot(dx, dy))

    def step(self, action: str) -> None:
        if action == "LEFT":
            self.agent.heading = wrap_angle(self.agent.heading - self.turn_size)
        elif action == "RIGHT":
            self.agent.heading = wrap_angle(self.agent.heading + self.turn_size)
        elif action == "FORWARD":
            self.agent.x += cos(self.agent.heading) * self.step_size
            self.agent.y += sin(self.agent.heading) * self.step_size
        else:
            raise ValueError(f"Unknown action: {action}")
