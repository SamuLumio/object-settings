"""
Automatic tkinter UI for the 'settings' package (object-settings)

(Tip: you can use set_padding() to match the padding of your application)
"""


_PADDING = 2

def pad():
	return _PADDING

def set_padding(padding: float):
	global _PADDING
	_PADDING = padding


from settings_gui._tk_abstractor import a

from . import main, section_frames, type_frames


from .main import SettingsFrame, SettingsWindow



def _reload_modules():
	import importlib
	for module in {main, section_frames, type_frames}:
		importlib.reload(module)


