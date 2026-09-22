from __future__ import annotations

from pathlib import Path
import pandas as pd

DATA = Path("data/flywire/fafb_v783")
OUT = Path("results")


def main() -> None:
    cls = pd.read_csv(DATA / "classification.csv.gz")
    types = pd.read_csv(DATA / "consolidated_cell_types.csv.gz")
    edges = pd.read_csv(DATA / "connections_princeton.csv.gz")
    meta = cls.merge(types, on="root_id", how="left")

    sources = meta[meta.primary_type.astype(str).str.match(r"^T[45][a-d]$", na=False)].copy()
    targets = meta[meta.primary_type.eq("DNa02")].copy()

    print("DNa02 targets:")
    print(targets[["root_id", "side", "primary_type", "additional_type(s)"]].to_string(index=False))
    if len(targets) != 2:
        raise RuntimeError(f"Expected bilateral DNa02 pair, found {len(targets)}")

    target_ids = set(targets.root_id)
    e2 = edges[edges.post_root_id.isin(target_ids)].copy()
    intermediates = set(e2.pre_root_id)

    e1 = edges[
        edges.pre_root_id.isin(set(sources.root_id))
        & edges.post_root_id.isin(intermediates)
    ].copy()

    srcmeta = sources[["root_id", "primary_type", "side"]].rename(
        columns={"root_id": "source_id", "primary_type": "source_type", "side": "source_side"}
    )
    tgtmeta = targets[["root_id", "side"]].rename(
        columns={"root_id": "target_id", "side": "target_side"}
    )

    # Join actual two-edge paths source -> intermediate -> DNa02.
    paths = e1.rename(columns={
        "pre_root_id": "source_id", "post_root_id": "intermediate_id",
        "syn_count": "syn1", "nt_type": "nt1", "neuropil": "neuropil1",
    }).merge(
        e2.rename(columns={
            "pre_root_id": "intermediate_id", "post_root_id": "target_id",
            "syn_count": "syn2", "nt_type": "nt2", "neuropil": "neuropil2",
        }),
        on="intermediate_id",
        how="inner",
    )
    paths = paths.merge(srcmeta, on="source_id").merge(tgtmeta, on="target_id")

    # A transparent path score for ranking only; not yet a neural model.
    # Geometric mean prevents one huge edge from masking a weak bottleneck.
    paths["path_score"] = (paths.syn1 * paths.syn2) ** 0.5

    summary = paths.groupby(
        ["source_type", "source_side", "target_side"], as_index=False
    ).agg(
        paths=("intermediate_id", "size"),
        intermediates=("intermediate_id", "nunique"),
        syn1_total=("syn1", "sum"),
        syn2_total=("syn2", "sum"),
        path_score=("path_score", "sum"),
    ).sort_values(["source_type", "source_side", "target_side"])

    print("\nTwo-hop T4/T5 -> DNa02 channel summary:")
    print(summary.to_string(index=False, float_format=lambda x: f"{x:.1f}"))

    print("\nTop individual two-hop paths:")
    show = paths.sort_values("path_score", ascending=False).head(60)
    print(show[[
        "source_type", "source_side", "source_id", "intermediate_id",
        "target_side", "target_id", "syn1", "nt1", "syn2", "nt2",
        "path_score",
    ]].to_string(index=False, float_format=lambda x: f"{x:.1f}"))

    OUT.mkdir(exist_ok=True)
    summary.to_csv(OUT / "t45_to_dna02_channels.csv", index=False)
    paths.to_csv(OUT / "t45_to_dna02_paths.csv", index=False)
    print("\nSaved results/t45_to_dna02_channels.csv")
    print("Saved results/t45_to_dna02_paths.csv")


if __name__ == "__main__":
    main()
