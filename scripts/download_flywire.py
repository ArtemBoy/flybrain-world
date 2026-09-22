from __future__ import annotations

import argparse
import gzip
import hashlib
import shutil
import urllib.request
from pathlib import Path

BASE = "https://codex.flywire.ai/api/download_resource"
DATASET = "fafb"
VERSION = 783
PRODUCTS = ("consolidated_cell_types", "connections_princeton")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download_product(product: str, out_dir: Path) -> Path:
    url = f"{BASE}?data_product={product}&dataset={DATASET}"
    gz_path = out_dir / f"{product}.csv.gz"
    csv_path = out_dir / f"{product}.csv"
    print(f"Downloading {product} ...")
    urllib.request.urlretrieve(url, gz_path)
    with gzip.open(gz_path, "rb") as src, csv_path.open("wb") as dst:
        shutil.copyfileobj(src, dst)
    print(f"  {csv_path} | sha256={sha256(csv_path)}")
    return csv_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("data/flywire/fafb_v783"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    print(f"FlyWire/Codex dataset: FAFB v{VERSION}")
    for product in PRODUCTS:
        download_product(product, args.out)


if __name__ == "__main__":
    main()
