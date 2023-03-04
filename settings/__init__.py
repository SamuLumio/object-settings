"""
Simple-to-use object-oriented config library.

The values have automatic validation and get saved to a file that's
seamlessly written and read in the background, so you don't have to worry about any of it.

PS: includes free GUIs with settings_gui
"""

from .config import config, setup, get_dir

from . import base, parser, types

from .base import Section, all_sections
from .types import *
