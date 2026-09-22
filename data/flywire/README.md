# FlyWire data provenance

## Pinned biological dataset

- Dataset: **FlyWire FAFB — Female Adult Fly Brain**
- Snapshot: **v783**
- Neurons reported by Codex: **139,255**
- Source: FlyWire/Codex, Princeton Neuroscience Institute
- Programmatic access: static Codex download resources
- Local directory: `data/flywire/fafb_v783/`

Large data files are intentionally excluded from Git. Run:

```bash
python scripts/download_flywire.py
```

The downloader retrieves the Codex `consolidated_cell_types` and
`connections_princeton` products and prints SHA-256 checksums. Record the
actual checksums before any experiment intended for publication/reproduction.

## Modeling baseline

Our initial dynamics will be based on Shiu et al., *Nature* 2024,
"A Drosophila computational brain model reveals sensorimotor processing."
That work uses leaky integrate-and-fire dynamics with FlyWire connectivity and
neurotransmitter identity. We will reproduce/validate a small known
sensorimotor transformation before using the model to control FlyBrain World.

## Scientific boundary

Downloading a connectome does **not** make `FlyWireBrain` a biological brain
simulation. We will label a controller connectome-driven only after:

1. world sensory state is encoded into documented biological input neurons;
2. activity propagates through FlyWire-derived directed synaptic connectivity;
3. LEFT/FORWARD/RIGHT is decoded only from documented biological output
   populations;
4. shuffled/disconnected controls are run.

Until then, the runnable UI continues to use `ToyBrain`.
