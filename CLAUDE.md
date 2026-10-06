# geoexp-units

Ready-made `geoexp.Hierarchy` instances. Read geoexp's `CLAUDE.md` first: its
code and testing conventions apply here unchanged (mypy --strict, NumPy
docstrings, no `print()` in library code, `ruff`).

## The one rule

**This package ships data, never logic.** `Hierarchy` and `aggregate_panel`
live in geoexp. If a hierarchy seems to need behaviour `Hierarchy` cannot
express, the fix is a proposal against geoexp, not code here.

## Adding a hierarchy

1. A module (`us.py`, ...) with a loader returning `geoexp.Hierarchy`.
2. Its data under `src/geoexp_units/data/<country>/`, with a provenance file.
3. A script in `scripts/` that regenerates the data from the primary source.
4. One entry in `_registry.py`.
5. Tests: row count, every level pair is a function, spot checks against the
   source.

Never fill a gap in source data with a guess: leave the unit out and warn, as
`br.ibge(legacy=True)` does.

## Things to confirm with the maintainer

Adding a dependency; changing a hierarchy's level names or key dtype (that is
a breaking change for users' joins); data whose licence is not clearly open.
