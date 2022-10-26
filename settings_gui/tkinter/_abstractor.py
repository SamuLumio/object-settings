import tkinter
import tkinter.ttk


class TtkAbstractor:
	def __init__(self):
		self._layer = tkinter.ttk

	@property
	def layer(self):
		return self._layer

	def switch_to_tkinter(self):
		self._layer = tkinter

	def switch_to_ttk(self):
		self._layer = tkinter.ttk

	def is_ttk(self):
		return self.layer == tkinter.ttk


a = TtkAbstractor()

a.switch_to_tkinter()
