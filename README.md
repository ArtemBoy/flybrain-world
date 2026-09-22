# FlyBrain World

An embodied connectome experiment: **can a fruit-fly connectome acquire a simple human-style skill and transfer it to a novel situation?**

## Current milestone — v0.3

The browser is now the **world and visualization layer only**. In BRAIN mode it sends sensory state to the local Python server:

```text
3D world → bearing + distance → Python BrainController → action → 3D world
```

The current Python controller is still `ToyBrain`, an engineering smoke test. There is **no decision policy in JavaScript**. This is the execution path that a future `FlyWireBrain` will replace.

> **Scientific status:** `ToyBrain` is not a biological fly-brain result. The API explicitly reports `biological: false`.

## Run

```bash
python serve.py
```

Then open the URL printed by the server (normally `http://localhost:8765`).

Optional port:

```bash
python serve.py --port 9000
```

If Windows blocks the requested port, the server chooses a free local port and prints it.

Use **W/A/D** or arrow keys in HUMAN mode, **B** for BRAIN mode, **H** for HUMAN mode, and **R** for a new target.

## Experiment 001 — Approach an object

A simulated agent senses only target bearing and distance. A swappable Python brain controller produces `LEFT`, `FORWARD`, or `RIGHT`; the world feeds the next sensory state back to the controller.

The command-line experiment remains available:

```bash
python -m experiments.experiment_001
python -m experiments.experiment_001 --seed 42
```

## What counts as success

1. The closed sensory → brain → action → world loop runs.
2. Randomized target positions are reproducible with seeds.
3. Brain implementations can be swapped without changing the world.
4. Biological data, modeling assumptions, and engineering mappings remain explicitly separated.
5. Before learning is added, a real-connectome controller must beat appropriate controls.

## Roadmap

- **v0.1** — toy closed-loop controller ✓
- **v0.2** — visual world + human PLAY baseline ✓
- **v0.3** — authoritative Python brain execution ✓
- **v0.4** — FlyWire connectome adapter
- **v0.5** — reward / biologically motivated plasticity
- **v0.6** — movable object + target zone
- **v1.0** — frozen-learning generalization and compositional-transfer experiments

Long-term embodiment target: FlyGym. Connectome data will be pinned to a specific FlyWire/Codex snapshot with provenance and checksums.

## Core research question

After learning separate object and destination relationships, can the connectome-driven agent execute a **novel combination it was never trained on**? That later test is the project's central target; the early milestones build the experimental machinery without prematurely claiming learning or cognition.
