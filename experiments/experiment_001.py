from __future__ import annotations

import argparse
import random
from brain.toy import ToyBrain
from world.arena import Arena, Target

def run(seed: int = 1, max_steps: int = 200, success_radius: float = 0.35) -> bool:
    rng = random.Random(seed)
    target = Target(rng.uniform(2.0, 5.0), rng.uniform(-3.0, 3.0))
    arena, brain = Arena(target), ToyBrain()
    print(f"Experiment 001 | seed={seed} | target=({target.x:.2f}, {target.y:.2f})")
    for step in range(max_steps):
        sensory = arena.sense()
        if sensory.distance <= success_radius:
            print(f"SUCCESS at step {step}; distance={sensory.distance:.3f}")
            return True
        action = brain.act(sensory)
        print(f"{step:03d} bearing={sensory.bearing:+.3f} distance={sensory.distance:.3f} action={action}")
        arena.step(action)
    print(f"FAIL after {max_steps} steps; distance={arena.sense().distance:.3f}")
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--max-steps", type=int, default=200)
    args = parser.parse_args()
    raise SystemExit(0 if run(args.seed, args.max_steps) else 1)
