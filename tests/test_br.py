"""Tests for the IBGE hierarchy, run against the shipped snapshot."""

from __future__ import annotations

import itertools

import polars as pl
import pytest
from geoexp import Hierarchy, aggregate_panel

from geoexp_units import br

CURRENT = ("municipio", "regiao_imediata", "regiao_intermediaria", "uf", "regiao")
LEGACY = ("municipio", "microrregiao", "mesorregiao", "uf", "regiao")


@pytest.fixture(scope="module")
def ibge() -> Hierarchy:
    return br.ibge()


def test_ibge_is_a_geoexp_hierarchy_over_the_current_division(ibge: Hierarchy) -> None:
    assert isinstance(ibge, Hierarchy)
    assert ibge.name == "br.ibge"
    assert ibge.levels == CURRENT
    assert "IBGE" in (ibge.source or "")


def test_ibge_covers_every_municipality(ibge: Hierarchy) -> None:
    # 5570 municipalities plus Boa Esperança do Norte (MT), created in 2023.
    assert ibge.frame.height >= 5570
    assert ibge.frame.get_column("uf").n_unique() == 27
    assert ibge.frame.get_column("regiao").n_unique() == 5


def test_every_coarser_level_is_a_function_of_every_finer_one(ibge: Hierarchy) -> None:
    # mapping() raises HierarchyError when a direction is not a function.
    for fine, coarse in itertools.combinations(CURRENT, 2):
        assert ibge.mapping(fine, coarse).height == ibge.frame.get_column(fine).n_unique()


@pytest.mark.parametrize(
    ("municipio", "uf_sigla", "regiao_nome"),
    [(3550308, "SP", "Sudeste"), (3304557, "RJ", "Sudeste"), (5300108, "DF", "Centro-Oeste")],
)
def test_spot_checks(ibge: Hierarchy, municipio: int, uf_sigla: str, regiao_nome: str) -> None:
    uf = dict(ibge.mapping("municipio", "uf", use_labels=True).rows())
    regiao = dict(ibge.mapping("municipio", "regiao", use_labels=True).rows())
    assert uf[municipio] == uf_sigla
    assert regiao[municipio] == regiao_nome


def test_labels_name_every_level(ibge: Hierarchy) -> None:
    assert set(ibge.labels) == set(CURRENT)
    assert ibge.labels["uf"] == "uf_sigla"


def test_aggregates_a_municipal_panel_to_states(ibge: Hierarchy) -> None:
    panel = pl.DataFrame(
        {"cod": [3550308, 3509502, 3304557], "t": [1, 1, 1], "y": [1.0, 2.0, 4.0]}
    ).with_columns(pl.col("cod").cast(pl.Int64))
    out = aggregate_panel(
        panel, unit="cod", time="t", outcome="y", hierarchy=ibge, to="uf", use_labels=True
    )
    assert dict(zip(out.get_column("uf"), out.get_column("y"), strict=True)) == {
        "RJ": 4.0,
        "SP": 3.0,
    }


def test_legacy_division_drops_uncovered_municipalities_loudly() -> None:
    with pytest.warns(UserWarning, match="Boa Esperança do Norte"):
        legacy = br.ibge(legacy=True)
    assert legacy.levels == LEGACY
    assert legacy.frame.get_column("microrregiao").null_count() == 0
    for fine, coarse in itertools.combinations(LEGACY, 2):
        legacy.mapping(fine, coarse)


def test_homonymous_labels_are_refused_rather_than_merged(ibge: Hierarchy) -> None:
    # "Itabaiana" is a regiao imediata in PB and in SE; aggregating by name
    # would add them together, so labels are refused and codes must be used.
    from geoexp.exceptions import HierarchyError

    with pytest.raises(HierarchyError, match="Itabaiana"):
        ibge.mapping("municipio", "regiao_imediata", use_labels=True)
    assert ibge.mapping("municipio", "regiao_imediata").height == ibge.frame.height
