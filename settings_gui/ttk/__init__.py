"""
Automatic ttk UI (based off of the tkinter variant) for the 'settings' package (object-settings)
"""

import settings_gui.tkinter

# noinspection PyProtectedMember
settings_gui.tkinter._abstractor.a.switch_to_ttk()
from settings_gui.tkinter import *


def disable_ttk():
	# noinspection PyProtectedMember
	settings_gui.tkinter._abstractor.a.switch_to_tkinter()
