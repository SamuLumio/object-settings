import settings

from . import type_frames, PAD
from ._abstractor import a




class SectionFrame(a.layer.Frame):
	def __init__(self, master, section: settings.Section, autosave=True):
		super().__init__(master)
		self.settings = []
		for setting in section.settings:
			frame = type_frames.types[type(setting)]
			self.settings.append(frame(self, setting, autosave=autosave))
			self.settings[-1].pack(fill='x', pady=PAD*2)

	def save_settings(self):
		for setting_frame in self.settings:
			setting_frame.save()
