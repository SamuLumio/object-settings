import os

import settings


download_options = settings.Section("Downloader settings")
settings.Number("Speed limit", 5, section=download_options)
settings.Path("Target directory", os.path.expanduser('~'), has_to_exist=True, section=download_options)
settings.Choice("Mirror", ["Europe", "Asia", "North America", "South America", "Africa"], "Asia", section=download_options)
settings.Multichoice("Files to download", ["Video", "Audio", "Subtitles"], ["Video", "Audio", "Subtitles"], section=download_options)

ui_options = settings.Section("UI settings")
settings.Toggle("Show file descriptions", True, ui_options)
settings.Choice("Speed measurement unit", ['Mbit', 'MB'], 'Mbit', ui_options)


def test_tkinter():

	import tkinter
	window = tkinter.Tk()
	window.title("Settings demo")

	import settings_gui.tkinter
	settings_gui.tkinter.SettingsFrame(window).pack(padx=5, pady=5, fill='both')

	window.mainloop()



def test_ttk():

	import tkinter
	window = tkinter.Tk()
	window.title("Settings demo")

	import settings_gui.ttk
	import sv_ttk
	sv_ttk.set_theme('dark')
	settings_gui.ttk.SettingsFrame(window).pack(padx=5, pady=5, fill='both')

	window.mainloop()
