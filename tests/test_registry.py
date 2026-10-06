"""Tests for the hierarchy registry."""

from __future__ import annotations

import pytest
from geoexp import Hierarchy

import geoexp_units


def test_available_lists_registered_hierarchies_with_descriptions() -> None:
    listed = geoexp_units.available()
    assert "br.ibge" in listed
    assert "IBGE" in listed["br.ibge"]


def test_load_returns_the_named_hierarchy_and_forwards_options() -> None:
    assert isinstance(geoexp_units.load("br.ibge"), Hierarchy)
    with pytest.warns(UserWarning):
        assert geoexp_units.load("br.ibge", legacy=True).levels[1] == "microrregiao"


def test_load_rejects_unknown_names_listing_the_known_ones() -> None:
    with pytest.raises(KeyError, match=r"br\.ibge"):
        geoexp_units.load("xx.nope")
