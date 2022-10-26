import settings

settings.setup("TestApp")

download_options = settings.Section("Downloader settings")
speed = settings.Number("Speed limit", 5, section=download_options)
dir = settings.Path("Target directory", '/home/yomama/Downloads', has_to_exist=True, section=download_options)
server = settings.Choice("Mirror", ["Europe", "Asia", "North America", "South America", "Africa"], "Asia", section=download_options)
files = settings.Multichoice("Files to download", ["Video", "Audio", "Subtitles"], ["Video", "Audio", "Subtitles"], section=download_options)

ui_options = settings.Section("UI settings")
show_descriptions = settings.Toggle("Show file descriptions", True, ui_options)
speed_unit = settings.Choice("Speed measurement unit", ['Mbit', 'MB'], 'Mbit', ui_options)





import tkinter
window = tkinter.Tk()
window.title("Settings demo")

import settings_gui.ttk
import sv_ttk
sv_ttk.set_theme('dark')
settings_gui.ttk.SettingsFrame(window).pack(padx=5, pady=5, fill='both')

window.mainloop()
