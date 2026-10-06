"""Regenerate ``src/geoexp_units/data/br/ibge_municipios.csv`` from the IBGE API.

Standard library only, so it runs anywhere Python does::

    python scripts/fetch_ibge.py

Source: IBGE, API de Localidades (``/api/v1/localidades/municipios``). IBGE
data is public; cite "Fonte: IBGE". The provenance line written next to the CSV
records the endpoint and the extraction date, and ``geoexp_units.br.ibge()``
exposes it as ``Hierarchy.source``.
"""

from __future__ import annotations

import csv
import datetime as dt
import gzip
import json
import pathlib
import urllib.request
from typing import Any

URL = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
OUT = pathlib.Path(__file__).resolve().parents[1] / "src" / "geoexp_units" / "data" / "br"

COLUMNS = [
    "municipio",
    "municipio_nome",
    "regiao_imediata",
    "regiao_imediata_nome",
    "regiao_intermediaria",
    "regiao_intermediaria_nome",
    "microrregiao",
    "microrregiao_nome",
    "mesorregiao",
    "mesorregiao_nome",
    "uf",
    "uf_sigla",
    "uf_nome",
    "regiao",
    "regiao_sigla",
    "regiao_nome",
]


def _row(m: dict[str, Any]) -> dict[str, Any]:
    imediata = m["regiao-imediata"]
    intermediaria = imediata["regiao-intermediaria"]
    uf = intermediaria["UF"]
    # Micro- and mesorregiões were frozen in 2017 and do not cover
    # municipalities created afterwards: those rows keep them empty.
    micro = m.get("microrregiao") or {}
    meso = micro.get("mesorregiao") or {}
    return {
        "municipio": m["id"],
        "municipio_nome": m["nome"],
        "regiao_imediata": imediata["id"],
        "regiao_imediata_nome": imediata["nome"],
        "regiao_intermediaria": intermediaria["id"],
        "regiao_intermediaria_nome": intermediaria["nome"],
        "microrregiao": micro.get("id", ""),
        "microrregiao_nome": micro.get("nome", ""),
        "mesorregiao": meso.get("id", ""),
        "mesorregiao_nome": meso.get("nome", ""),
        "uf": uf["id"],
        "uf_sigla": uf["sigla"],
        "uf_nome": uf["nome"],
        "regiao": uf["regiao"]["id"],
        "regiao_sigla": uf["regiao"]["sigla"],
        "regiao_nome": uf["regiao"]["nome"],
    }


def main() -> None:
    """Fetch every municipality and write the CSV plus its provenance line."""
    with urllib.request.urlopen(URL, timeout=120) as response:
        body = response.read()
    # The endpoint gzips its body even when the request does not ask for it.
    if body[:2] == b"\x1f\x8b":
        body = gzip.decompress(body)
    data = json.loads(body.decode("utf-8"))
    rows = sorted((_row(m) for m in data), key=lambda r: r["municipio"])
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "ibge_municipios.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (OUT / "ibge_municipios.source.txt").write_text(
        f"IBGE, API de Localidades ({URL}), extracted {dt.date.today().isoformat()}\n",
        encoding="utf-8",
    )
    print(f"wrote {len(rows)} municipalities to {OUT}")


if __name__ == "__main__":
    main()
