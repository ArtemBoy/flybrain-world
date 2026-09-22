from __future__ import annotations

from pathlib import Path
import pandas as pd

DATA = Path("data/flywire/fafb_v783")
MAX_HOPS = 4
TOP = 30


def main() -> None:
    cls = pd.read_csv(DATA / "classification.csv.gz")
    types = pd.read_csv(DATA / "consolidated_cell_types.csv.gz")
    edges = pd.read_csv(DATA / "connections_princeton.csv.gz")

    meta = cls.merge(types, on="root_id", how="left")
    t45 = meta[meta["primary_type"].astype(str).str.match(r"^T[45][a-d]$", na=False)]
    dns = meta[(meta["super_class"] == "descending") & (meta["flow"] == "efferent")]

    source_ids = set(t45.root_id.astype("int64"))
    dn_ids = set(dns.root_id.astype("int64"))

    print(f"T4/T5 sources: {len(source_ids):,}")
    print(t45.groupby(["primary_type", "side"]).size().to_string())
    print(f"\nDescending targets: {len(dn_ids):,}")
    print(dns.groupby("side").size().to_string())

    # Keep all edges for reachability, but aggregate duplicate pre->post neuropil
    # rows when reporting strength.
    frontier = source_ids
    seen = set(source_ids)
    reached_records = []

    for hop in range(1, MAX_HOPS + 1):
        step = edges[edges.pre_root_id.isin(frontier)]
        next_ids = set(step.post_root_id.astype("int64"))
        reached = next_ids & dn_ids

        print(
            f"\nhop {hop}: frontier={len(frontier):,} "
            f"edges={len(step):,} next={len(next_ids):,} "
            f"new_descending={len(reached):,}"
        )

        if reached:
            hit_edges = step[step.post_root_id.isin(reached)].copy()
            summary = (
                hit_edges.groupby(["post_root_id", "nt_type"], as_index=False)
                .agg(syn_count=("syn_count", "sum"), upstream_edges=("pre_root_id", "nunique"))
                .sort_values(["syn_count", "upstream_edges"], ascending=False)
            )
            summary = summary.merge(
                dns[["root_id", "side", "primary_type", "additional_type(s)"]],
                left_on="post_root_id", right_on="root_id", how="left"
            )
            summary["hop"] = hop
            reached_records.append(summary)
            print("\nStrongest descending hits:")
            print(summary[[
                "post_root_id", "side", "primary_type", "additional_type(s)",
                "nt_type", "syn_count", "upstream_edges"
            ]].head(TOP).to_string(index=False))

        frontier = next_ids - seen
        seen |= next_ids
        if not frontier:
            break

    if reached_records:
        out = pd.concat(reached_records, ignore_index=True)
        out.to_csv("results/t45_to_descending_candidates.csv", index=False)
        print("\nSaved results/t45_to_descending_candidates.csv")
    else:
        print("\nNo descending neurons reached within hop limit.")


if __name__ == "__main__":
    Path("results").mkdir(exist_ok=True)
    main()
