"""
Automatic ttk UI (based off of the tkinter variant) for the 'settings' package (object-settings)

(Tip: you can use set_padding() to match the padding of your application)
"""


import settings_gui._tk_abstractor as _abstractor

from settings_gui.tkinter import *




def enable_ttk():
	_abstractor.a.switch_to_ttk()
	_reload()


def disable_ttk():
	# noinspection PyProtectedMember
	_abstractor.a.switch_to_tkinter()
	_reload()

def _reload():
	import importlib
	import settings_gui.tkinter
	settings_gui.tkinter._reload_modules()
	importlib.reload(settings_gui.tkinter)
	importlib.reload(__import__(__name__))
	exec('from settings_gui.tkinter import *', globals())



if not _abstractor.a.is_ttk():
	enable_ttk()
