"""Module for calculating fiber reinforced composites properties."""
from .io.text import text_output
from .io.parser import parse, info, warn
from .core.fiber import fiber
from .core.resin import resin
from .core.lamina import lamina
from .core.laminate import laminate
from .version import __version__, __license__
