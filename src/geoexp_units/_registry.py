"""Name -> loader registry for the shipped hierarchies.

Adding a hierarchy is one entry here plus its module and data: nothing in
geoexp changes, because every loader returns a plain ``geoexp.Hierarchy``.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from geoexp import Hierarchy

from geoexp_units import br

#: name -> (loader, one-line description).
_REGISTRY: dict[str, tuple[Callable[..., Hierarchy], str]] = {
    "br.ibge": (
        br.ibge,
        "Brazil, IBGE: municipio -> regiao imediata -> intermediaria -> UF -> regiao "
        "(legacy=True: micro/mesorregiao)",
    ),
}


def available() -> dict[str, str]:
    """List the registered hierarchies and what each one is.

    Returns
    -------
    dict of str to str
        Name -> one-line description.
    """
    return {name: description for name, (_, description) in _REGISTRY.items()}


def load(name: str, **options: Any) -> Hierarchy:
    """Load a registered hierarchy by name.

    Parameters
    ----------
    name : str
        A name from :func:`available`, e.g. ``"br.ibge"``.
    **options
        Forwarded to the loader, e.g. ``legacy=True``.

    Returns
    -------
    geoexp.Hierarchy

    Raises
    ------
    KeyError
        If ``name`` is not registered; the message lists the known names.
    """
    if name not in _REGISTRY:
        raise KeyError(f"unknown hierarchy {name!r}; available: {sorted(_REGISTRY)}")
    loader, _ = _REGISTRY[name]
    return loader(**options)
