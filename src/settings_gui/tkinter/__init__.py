"""
Automatic tkinter UI for the 'settings' package (object-settings)
"""



from settings_gui._tk_abstractor import a

from . import lib,  main, section_frames, type_frames


from .main import SettingsFrame, SettingsWindow



def _reload_modules():
	import importlib
	for module in {lib, main, section_frames, type_frames}:
		importlib.reload(module)


