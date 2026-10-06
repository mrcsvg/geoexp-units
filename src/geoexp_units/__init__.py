"""geoexp-units: ready-made unit hierarchies for geoexp.

Every hierarchy here is a plain ``geoexp.Hierarchy``, ready for
``geoexp.aggregate_panel``. Discover them with :func:`available` and load one
with :func:`load` or its module function (e.g. ``geoexp_units.br.ibge()``).
"""

from geoexp_units import br
from geoexp_units._registry import available, load
from geoexp_units._version import __version__

__all__ = ["__version__", "available", "br", "load"]
