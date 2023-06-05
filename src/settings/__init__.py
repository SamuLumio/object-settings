"""
Simple-to-use object-oriented config library.

The values have automatic validation and get saved to a file that's
seamlessly written and read in the background, so you don't have to worry about any of it.

PS: includes free GUIs with settings_gui
"""

from . import backend
from .backend import config, setup
from . import base
from .base import Section, all_sections, BaseSetting
from . import types
from .types import *
