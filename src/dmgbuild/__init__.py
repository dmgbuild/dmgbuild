from importlib.metadata import version

from .core import build_dmg

__version__ = version("dmgbuild")

__all__ = ["__version__", "build_dmg"]
