import os, typing, colorsys, settings, subprocess, tkinter.filedialog
import tkinter as tk

from ..config import config, strings
from . import a, lib



class _Base(a.layer.Frame): # type: ignore
	def __init__(self, master, setting: settings.BaseSetting, autosave: bool, width_limit=30):
		super().__init__(master)
		settings.BaseSetting
		self.setting = setting
		self.variable = tk.Variable()
		self.widget: a.layer.Widget | None = None # type: ignore
		self.autosave = autosave
		self.width_limit = width_limit

		self.error_photoimage = lib.Icon('error')
		self.error_icon = lib.AppearingWidget(a.layer.Label(self, image=self.error_photoimage))

		a.layer.Label(self, text=setting.name).pack(side='left', padx=config.padding)
		a.layer.Frame(self).pack(side='left', padx=config.padding*3)

		self.init()

		# Settings set from envvars can't be changed
		if self.setting.set_externally:
			self.widget = a.layer.Label(self, text=strings.set_from_env, foreground='gray')

		if isinstance(self.widget, a.layer.Widget):
			self.widget: a.layer.Widget # type: ignore
			self.widget.pack(side='right', padx=config.padding)

		if isinstance(self.widget, (a.layer.Entry, a.layer.Spinbox, a.layer.OptionMenu)):
			self.variable.trace_add('write', self.update_width)
			self.variable.trace_add('write', self.validate)

		self.update_variable()
		self.setting.add_listener(self.update_variable)


	def init(self):
		"""For faster subclassing"""


	def set_error(self, error: bool):
		if error:
			self.error_icon.show()
			if a.is_ttk():
				self.widget.state(["invalid"])
		else:
			self.error_icon.hide()
			if a.is_ttk():
				self.widget.state(["!invalid"])


	def validate(self, *dummy_args):
		result = self.setting.validate(self.variable.get())
		self.set_error(not result)

	def update_variable(self, *dummy_args):
		if self.setting.get() != self.variable.get():
			self.variable.set(self.setting.get())


	def update_width(self, *dummy_args):
		try:
			width = len(str(self.variable.get())) + 1
			# if a.is_ttk() and isinstance(self.widget, a.layer.Spinbox):
			# 	width += 3
			if width < self.width_limit:
				self.widget.configure(width=width)
		except tk.TclError:
			pass


	def save(self):
		if self.setting.get() != self.variable.get():
			if not self.setting.set_externally:
				try:
					self.setting.set(self.variable.get())
					self.set_error(False)
				except (ValueError, tk.TclError):
					self.set_error(True)


	def save_from_widget(self, *args):
		if self.autosave:
			self.save()





class Toggle(_Base):
	"""A checkbutton, or a switch if available from ttk theme"""
	def init(self):
		self.variable = tk.BooleanVar()
		self.widget = a.layer.Checkbutton(self, variable=self.variable, command=self.save_from_widget)
		if a.is_ttk():
			self.widget.configure(style='Switch.TCheckbutton')





class Choice(_Base):
	"""A horizontal radiobutton-row or an expandable menu, depending on the number of options"""
	def init(self):
		self.setting: settings.Choice
		self.variable = tk.StringVar()
		options_size = lib.calculate_options_size(self.setting.options)
		if options_size <= self.width_limit:
			frame = a.layer.Frame(self)
			for option in reversed(self.setting.options):
				a.layer.Radiobutton(frame, text=option, value=option, variable=self.variable,
									command=self.save_from_widget).pack(side='right', padx=config.padding)
			self.widget = frame
		else:
			self.widget = a.layer.OptionMenu(self, self.variable, self.setting.value, *self.setting.options,
											 command=self.save_from_widget)





class Multichoice(_Base):
	"""Either a horizontal or vertical checkbutton-row, depending on the number of options"""
	def init(self):
		self.setting: settings.Multichoice
		self.variable = self.MultichoiceVar(self.setting.options)
		self.widget = a.layer.Frame(self)
		options_size = lib.calculate_options_size(self.setting.options)
		direction = 'left' if options_size <= self.width_limit else 'top'

		for option in self.setting.options:
			a.layer.Checkbutton(self.widget, text=option, variable=self.variable[option],
								command=self.save_from_widget).pack(side=direction, anchor='w',
																	padx=config.padding / 2)

	class MultichoiceVar:
		def __init__(self, options: list):
			super().__init__()
			self.variables = {}
			for option in options:
				self.variables[option] = tk.BooleanVar()

		def get(self):
			return [option for option, value in self.variables.items() if value.get()]

		def set(self, value: list):
			for item in self.variables.keys():
				self.variables[item].set(item in value)

		def __getitem__(self, item):
			return self.variables[item]





class Text(_Base):
	"""Entry field with an appearing done-button (if autosave)"""
	def init(self):
		self.variable = tk.StringVar()
		self.widget = a.layer.Entry(self, textvariable=self.variable)
		self.done_button = lib.AppearingWidget(lib.icon_button(self, 'checkmark', self.save_from_widget))

		if self.autosave:
			self.variable.trace_add('write', lambda *args: self.show_done_button())

	def show_done_button(self):
		if self.variable.get() != self.setting.get():
			self.done_button.show()

	def save_from_widget(self, *args):
		super().save_from_widget(*args)
		self.done_button.hide()





class Path(Text):
	"""Like Text, but with a button to open a file chooser"""
	def init(self):
		super().init()
		if not self.setting.set_externally:
			lib.icon_button(self, 'folder', self.browse).pack(side='right', padx=config.padding)

	def browse(self):
		try:
			out = subprocess.run(['zenity', '--file-selection'], capture_output=True)
			dir = out.stdout.decode().strip()
			if dir:
				self.variable.set(dir)
		except FileNotFoundError:
			def open(func):
				dir = func(initialdir=os.path.expanduser('~'))
				if dir:
					self.variable.set(dir)
			popup = tk.Menu(self, tearoff=False)
			popup.add_command(label=strings.file, command=lambda: open(tkinter.filedialog.askopenfilename))
			popup.add_command(label=strings.dir, command=lambda: open(tkinter.filedialog.askdirectory))
			popup.tk_popup(*self.winfo_pointerxy())





class Number(_Base):
	"""Spinbox that allows to increment/decrement (or manually type in)"""
	def init(self):
		self.setting: settings.Number
		self.variable = tk.IntVar()
		self.widget = a.layer.Spinbox(self, textvariable=self.variable,
									  from_=self.setting.lower_limit, to=self.setting.upper_limit)
		self.variable.trace_add('write', self.save_from_widget)





class Float(_Base):
	"""Spinbox that allows to increment/decrement (or manually type in)"""

	def init(self):
		self.setting: settings.Float
		self.variable = tk.DoubleVar()
		self.variable_prev_value = self.variable.get()
		self.variable_prev_value_next = self.variable.get()
		self.widget = a.layer.Spinbox(
			self,
			textvariable=self.variable,
			from_=self.setting.lower_limit,
			to=self.setting.upper_limit,
			increment=self.setting.step_size,
			format=f'%.{self.setting.precision}f'
		)
		self.variable.trace_add('write', self.save_from_widget)


		






types = {
	settings.Toggle: Toggle,
	settings.Text: Text,
	settings.Choice: Choice,
	settings.MappedChoice: Choice,
	settings.Multichoice: Multichoice,
	settings.Path: Path,
	settings.Number: Number,
	settings.Float: Float
}
