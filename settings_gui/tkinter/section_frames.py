import settings

from . import type_frames, PAD
from ._abstractor import a




class SectionFrame(a.layer.Frame):
	def __init__(self, master, section: settings.Section, autosave=True):
		super().__init__(master)
		self.settings = []
		for setting in section.settings:
			for type, type_frame in type_frames.types.items():
				if isinstance(setting, type):
					frame = type_frame(setting)
					self.settings.append(frame(self, setting, autosave=autosave))
					self.settings[-1].pack(fill='x', pady=PAD*2)
					break

	def save_settings(self):
		for setting_frame in self.settings:
			setting_frame.save()
