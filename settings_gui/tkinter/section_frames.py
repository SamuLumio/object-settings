import settings

from . import type_frames, pad, a




class SectionFrame(a.layer.Frame):
	def __init__(self, master, section: settings.Section, autosave=True):
		super().__init__(master)
		self.settings = []
		self._pad()
		for setting in section.settings:
			for type, type_frame in type_frames.types.items():
				if isinstance(setting, type):
					self.settings.append(type_frame(self, setting, autosave=autosave))
					self.settings[-1].pack(fill='x', pady=pad()*2, padx=pad()*2)
					break
		self._pad()


	def _pad(self):
		a.layer.Frame(self).pack(pady=pad()/2)

	def save_settings(self):
		for setting_frame in self.settings:
			setting_frame.save()
