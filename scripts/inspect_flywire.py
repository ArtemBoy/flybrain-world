from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd

DATA = Path("data/flywire/fafb_v783")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def counts(df: pd.DataFrame, column: str, n: int = 40) -> None:
    print(f"\n--- {column} ({df[column].nunique(dropna=True)} unique) ---")
    print(df[column].value_counts(dropna=False).head(n).to_string())


def main() -> None:
    files = {
        "classification": DATA / "classification.csv.gz",
        "types": DATA / "consolidated_cell_types.csv.gz",
        "neurons": DATA / "neurons.csv.gz",
        "connections": DATA / "connections_princeton.csv.gz",
    }

    print("FAFB v783 local fingerprints")
    for name, path in files.items():
        print(f"{name:15s} {path.stat().st_size:12,d} bytes  sha256={digest(path)}")

    cls = pd.read_csv(files["classification"])
    types = pd.read_csv(files["types"])
    neurons = pd.read_csv(files["neurons"])

    print(f"\nclassification rows: {len(cls):,}")
    print(f"cell-type rows:      {len(types):,}")
    print(f"neuron rows:         {len(neurons):,}")

    for col in ("flow", "super_class", "class", "sub_class", "side", "nerve"):
        counts(cls, col)

    # Candidate output populations: print every hierarchy value containing
    # descending/motor-like terms, without assuming Codex's exact vocabulary.
    terms = r"descend|motor|DN|neck|leg|wing"
    mask = pd.Series(False, index=cls.index)
    for col in ("super_class", "class", "sub_class"):
        mask |= cls[col].astype(str).str.contains(terms, case=False, regex=True)
    candidates = cls.loc[mask].copy()
    print(f"\n=== OUTPUT CANDIDATES ({len(candidates):,} rows) ===")
    if len(candidates):
        print(candidates.groupby(
            ["flow", "super_class", "class", "sub_class", "side"],
            dropna=False
        ).size().sort_values(ascending=False).head(100).to_string())

    # Visual candidates from hierarchy plus named cell types.
    visual_mask = (
        cls["super_class"].astype(str).str.contains("optic|visual", case=False, regex=True)
        | cls["class"].astype(str).str.contains("optic|visual", case=False, regex=True)
    )
    visual = cls.loc[visual_mask]
    print(f"\n=== VISUAL/OPTIC HIERARCHY ({len(visual):,} rows) ===")
    print(visual.groupby(
        ["flow", "super_class", "class", "sub_class", "side"],
        dropna=False
    ).size().sort_values(ascending=False).head(100).to_string())

    # Named motion-sensitive families that are immediately relevant to turning.
    named = types[
        types["primary_type"].astype(str).str.match(r"^(T4|T5|HS|VS)", case=False, na=False)
    ]
    print(f"\n=== NAMED MOTION-SENSITIVE TYPE CANDIDATES ({len(named):,}) ===")
    print(named["primary_type"].value_counts().head(100).to_string())


if __name__ == "__main__":
    main()
