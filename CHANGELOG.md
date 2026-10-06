# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `geoexp_units.br.ibge()`: the IBGE territorial division as a
  `geoexp.Hierarchy` — `municipio -> regiao_imediata -> regiao_intermediaria ->
  uf -> regiao`, with labels, keyed by the 7-digit code. `legacy=True` gives
  `microrregiao -> mesorregiao` instead, leaving out (with a warning) the
  municipalities IBGE never assigned one.
- Snapshot of the IBGE API de Localidades (5571 municipalities, extracted
  2026-09-25) and `scripts/fetch_ibge.py` to regenerate it.
- `available()` / `load()` registry.

### How Claude was used

Designed with the maintainer in the geoexp 0.2 session (see geoexp's
`docs/design-2026-09-25-0.2-api.md`): the maintainer chose to ship hierarchies
as a separate package and chose the name. Claude Code wrote the code, tests
and fetch script, ran the fetch, and found that the legacy division does not
cover municipalities created after 2017, which became the `legacy=True`
behaviour. Nothing here was committed or published by Claude.
