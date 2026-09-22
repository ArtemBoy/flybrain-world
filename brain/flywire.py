from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from brain.base import BrainController, SensoryState


@dataclass(frozen=True)
class FlyWireDataset:
    name: str = "FAFB"
    version: int = 783
    neuron_count: int = 139_255
    codex_dataset: str = "fafb"
    data_dir: Path = Path("data/flywire/fafb_v783")


DATASET = FlyWireDataset()


class FlyWireBrain(BrainController):
    """Future connectome-backed controller.

    v0.4 starts by pinning data provenance and validating the biological
    input/output populations. It deliberately refuses to act until actual
    FlyWire connectivity is loaded and causally used for action selection.
    """

    biological = True

    def __init__(self, data_dir: Path = DATASET.data_dir) -> None:
        self.data_dir = Path(data_dir)
        raise RuntimeError(
            "FlyWireBrain is not executable yet. "
            "Download/validate FAFB v783 and define biological sensory/output populations first."
        )

    def act(self, sensory: SensoryState) -> str:
        raise NotImplementedError
