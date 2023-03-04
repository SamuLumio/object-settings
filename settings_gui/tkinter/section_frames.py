import settings

from ..config import config
from . import type_frames, a




class SectionFrame(a.layer.Frame):
	def __init__(self, master, section: settings.Section, autosave=True):
		super().__init__(master)
		self.settings = []
		self._pad()
		for setting in section.settings:
			for type, type_frame in type_frames.types.items():
				if isinstance(setting, type):
					self.settings.append(type_frame(self, setting, autosave=autosave))
					self.settings[-1].pack(fill='x', pady=config.padding*2, padx=config.padding*2)
					break
		self._pad()


	def _pad(self):
		a.layer.Frame(self).pack(pady=config.padding/2)

	def save_settings(self):
		for setting_frame in self.settings:
			setting_frame.save()
