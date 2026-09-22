# FlyBrain World

An embodied connectome experiment: **can a fruit-fly connectome acquire a simple human-style skill and transfer it to a novel situation?**

## Experiment 001 — Approach an object

The first milestone is intentionally small. A simulated agent senses only target bearing and distance. A swappable brain controller produces `LEFT`, `FORWARD`, or `RIGHT`; the world then feeds the next sensory state back to the controller.

> **Scientific status:** the initial `ToyBrain` is an engineering smoke test, **not a biological fly-brain result**. The real FlyWire connectome will enter through the same `BrainController` interface.

## Run v0.1

```bash
python -m experiments.experiment_001
python -m experiments.experiment_001 --seed 42
```

No third-party packages are required yet.

## What counts as success

1. The closed sensory → brain → action → world loop runs.
2. Randomized target positions are reproducible with seeds.
3. Brain implementations can be swapped without changing the world.
4. Biological data, modeling assumptions, and engineering mappings remain explicitly separated.
5. Before learning is added, a real-connectome controller must beat appropriate controls.

## Roadmap

- **v0.1** — toy closed-loop controller (current)
- **v0.2** — visual world + human `PLAY` baseline
- **v0.3** — FlyWire connectome adapter
- **v0.4** — reward / biologically motivated plasticity
- **v0.5** — movable object + target zone
- **v1.0** — frozen-learning generalization and compositional-transfer experiments

Long-term embodiment target: FlyGym 2.x. Connectome data will be pinned to a specific FlyWire/Codex snapshot with provenance and checksums.

## Core research question

After learning separate object and destination relationships, can the connectome-driven agent execute a **novel combination it was never trained on**? That later test is the project's central target; v0.1 exists to build the experimental machinery without prematurely claiming learning or cognition.

## Visual demo (v0.2)

Start the local server:

```bash
python serve.py
```

Then open `http://localhost:8000`. Use **W/A/D** or arrow keys in HUMAN mode, **B** for BRAIN mode, **H** for HUMAN mode, and **R** for a new target.

The v0.2 browser BRAIN mode intentionally mirrors `ToyBrain` only as a UI prototype. **It is not the future connectome execution path.** The next integration routes sensory observations to Python so the browser becomes visualization/embodiment only and the authoritative brain controller remains in Python.
