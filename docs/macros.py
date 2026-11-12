"""Template variables for the dmgbuild documentation.

Loaded by the Zensical ``macros`` extension (see ``zensical.toml``).
"""

from importlib.metadata import version


def define_env(env):
    # The full version, including alpha/beta/rc tags.
    env.variables["release"] = version("dmgbuild")
