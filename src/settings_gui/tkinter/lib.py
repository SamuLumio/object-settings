import typing, os, colorsys, tkinter

from ..config import config
from . import a



class Icon(tkinter.PhotoImage):
	"""Tkinter PhotoImage with automatically generated path for object-settings"""
	
	def __init__(self, name: str, color: typing.Literal['black', 'white'] | None = None):
		filename = name
		if color: filename += '-' + color
		filename += '.png'
		path = os.path.join(os.path.dirname(__file__), 'icons', filename)
		super().__init__(file=path)
		self._created_icons.append(self)

	_created_icons = []
	"""List of all created icons – required for tkinter to persist them"""



class AppearingWidget:
	"""Show and hide any tkinter widget"""

	def __init__(self, widget: a.layer.Widget): # type: ignore
		self.widget = widget
		self.visible = False

	def show(self):
		if not self.visible:
			self.widget.pack(side='right', padx=config.padding*2)
			self.visible = True

	def hide(self):
		if self.visible:
			self.widget.forget()
			self.visible = False



# Generator function instead of a class, because a.layer reference needs to change
def icon_button(master, icon_name: str, command):
	"""Generate a (normal or ttk) button with an icon of the correct color"""
	
	if a.is_ttk():
		hex = a.layer.Style().lookup('TButton', 'background') # type: ignore
		hex = str(hex).removeprefix('#')
		rgb = tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))
		hls = colorsys.rgb_to_hls(*rgb)
		brightness = hls[1]
		color = 'black' if brightness > 50 else 'white'
	else:
		color = 'black'

	icon_image = Icon(icon_name, color)
	#self.icons.append(icon_image)
	return a.layer.Button(master, image=icon_image, command=command)



def calculate_options_size(options: list[str]):
	"""Calculate roughly the size taken up by options' labels and their icons/checkmarks"""
	text = sum(len(o) for o in options)
	icons = len(options) * 3
	return text + icons
