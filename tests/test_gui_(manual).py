import os, appdirs

import settings


download_options = settings.Section("Downloader settings")
settings.Number("Speed limit", 5, section=download_options)
settings.Path("Target directory", os.path.expanduser('~'), has_to_exist=True, section=download_options)
settings.Choice("Mirror", ["Europe", "Asia", "North America", "South America", "Africa"], "Asia", section=download_options)
settings.Multichoice("Files to download", ["Video", "Audio", "Subtitles"], ["Video", "Audio", "Subtitles"], section=download_options)

ui_options = settings.Section("UI settings")
settings.Toggle("Show file descriptions", True, ui_options)
settings.Choice("Speed measurement unit", ['Mbit', 'MB'], 'Mbit', ui_options)

advanced = settings.Section("Advanced")
settings.Path("Data directory", "set from env so you shouldn't see this", section=advanced)
os.environ['TESTAPP_DATA_DIRECTORY'] = appdirs.user_data_dir()


def test_tkinter():

	import tkinter
	window = tkinter.Tk()
	window.title("Check that tkinter GUI looks right")

	import settings_gui.tkinter
	settings.base.default_section.settings.clear()
	frame = settings_gui.tkinter.SettingsFrame(window)
	assert isinstance(frame, tkinter.Frame)
	frame.pack(padx=5, pady=5, fill='both')

	window.mainloop()



def test_ttk():

	import tkinter.ttk
	window = tkinter.Tk()
	window.title("Check that ttk GUI looks right")

	import sv_ttk
	sv_ttk.set_theme('dark')

	import settings_gui.ttk
	settings_gui.config.config(padding=4)
	tkinter.ttk.Frame(window).pack(pady=2)
	settings.base.default_section.settings.clear()
	frame = settings_gui.ttk.SettingsFrame(window)
	assert isinstance(frame, tkinter.ttk.Frame)
	for section in frame.sections:
		section.configure(style='Card.TFrame')
	frame.pack(padx=5, pady=5, fill='both')

	window.mainloop()

	settings_gui.ttk.disable_ttk()
