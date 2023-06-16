import settings, tkinter, typing

from ..config import config, strings
from . import section_frames, a


class SettingsFrame(a.layer.Frame): # type: ignore
	def __init__(self, master, autosave=True, save_button=False):
		super().__init__(master)
		self.sections = []

		for section in settings.all_sections:
			if section.settings != []:
				a.layer.Frame(self).pack(pady=config.padding)  # for padding
				a.layer.Label(self, text=section.name, font='big').pack(padx=config.padding)
				section_frame = section_frames.SectionFrame(self, section, autosave=autosave)
				section_frame.pack(fill='x', expand=True, padx=2*config.padding, pady=3*config.padding)
				self.sections.append(section_frame)

		if isinstance(save_button, str):
			save_text = save_button  # For backwards compatibility
		else:
			save_text = strings.save

		if save_button:
			button = a.layer.Button(self, command=self.save_settings, text=save_text)
			if a.is_ttk():
				button.configure(style='Accent.TButton')  # type: ignore
			button.pack(pady=config.padding*3)

	def save_settings(self):
		for section_frame in self.sections:
			section_frame.save_settings()
		if isinstance(self.master, SettingsWindow):
			self.master.destroy()



class SettingsWindow(tkinter.Toplevel):
	def __init__(self, master, title="Settings", autosave=True, save_button=False):
		super().__init__(master)
		SettingsFrame(self, autosave, save_button).pack(padx=config.padding*2, pady=config.padding*2, fill='both')

		self.title(title)
	#	self.minsize(self.winfo_width(), self.winfo_height())
		self.resizable(False, False)
