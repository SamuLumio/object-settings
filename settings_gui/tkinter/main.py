import settings, tkinter

from . import section_frames, PAD
from ._abstractor import a


class SettingsFrame(a.layer.Frame):
	def __init__(self, master, autosave=True, save_button: str = None):
		super().__init__(master)
		self.sections = []
		for section in settings.all_sections:

			if section != settings.base.default_section:
				a.layer.Label(self, text=section.name, font='big').pack(padx=PAD)

			self.sections.append(section_frames.SectionFrame(self, section, autosave=autosave))
			self.sections[-1].pack(fill='x', expand=True, padx=PAD * 2, pady=PAD * 2)

		if isinstance(save_button, str):
			button = a.layer.Button(self, command=self.save_settings, text=save_button)
			if a.is_ttk():
				button.configure(style='Accent.TButton')
			button.pack(pady=PAD*3)

	def save_settings(self):
		for section_frame in self.sections:
			section_frame.save_settings()
		if isinstance(self.master, SettingsWindow):
			self.master.destroy()



class SettingsWindow(tkinter.Toplevel):
	def __init__(self, master, title="Settings", autosave=True, save_button: str = None):
		super().__init__(master)
		SettingsFrame(self, autosave, save_button).pack(padx=PAD*2, pady=PAD*2, fill='both')

		self.title(title)
	#	self.minsize(self.winfo_width(), self.winfo_height())
		self.resizable(False, False)
