
object-settings
===============

Simple-to-use object-oriented Python config library, where your settings are objects.

Their values have automatic validation and get saved to a file that's seamlessly written and read in the background, so you don't have to worry about any of it. This makes it quick to define and use settings (see examples below).



## Installation & usage

This package is on PyPi, so you can just do `pip install object-settings`

After which it will be available with just the module name `settings`

```python
import settings
settings.setup("Your app name")
    
your_option1 = settings.Toggle("Your first option label")
your_option2 = settings.Number("Your second option label")
```



## Just simple objects

For example, you can set a font size at the top of your ui file:

```python
font = settings.Number(default=14)

...
someuilib.Label("Bababooey", size=font.value)
...
someuilib.Textbox("Lorem ipsum dolor...", font_size=font.value)
...
```

Or if a setting is only checked in one place, it can be used without defining a variable:

```python
if settings.Toggle("Update app automatically", default=True):
    # do update
```

(it doesn't matter if the same setting is initialized multiple times)



## Integration

The setting objects support "equals"-checking with actual values:

```python
speed = settings.Number("Speed limit", 5)

print(speed == 5)
>> True
print(speed == 3)
>> False
```

In addition, they work with many type-specific operations:

```python
for selection in settings.Multichoice():
    ...

if settings.Toggle():
    ...
```



## Automatic storing

When a setting's value is read/set, object-settings automatically creates and updates a config file on the disk in the background. It can read many file types, like `.cfg`, `.json` and `.yaml`. Any file deletions or unparsable external modifications are also handled.

By default, the files are saved to a standard config location, depending on the platform (uses [appdirs](https://github.com/ActiveState/appdirs) package for paths). You can also set a custom directory for e.g. running in a Docker container.

Setting values are also automatically read from the environment, like from env vars or command line options. The under-the-hood parser system is also very extensible, so you can create and add custom ones for e.g. a custom database.



## Value validation

When a new value is set, it automatically gets validated and raises a `ValueError` if it doesn't pass:

```python
update_interval = settings.Number("Update interval", default=5)
update_interval.set("Daily")
>> ValueError
```

This validation includes more than just datatypes, for example numbers can have min/max limits, or a path setting can be set to require an existing path:

```python
path = settings.Path("Download path", has_to_exist=True)
path.set("/nonexistent/directory")
>> ValueError
```



## Listen for changes

If you have some update function that you want to be called when a setting is changed, you can add that function as a listener:

```python
some_setting.add_listener(your_function)
```

Now the function will be called every time when a new value is set.



## Sections

Optionally, if you have a lot of settings, you can organize them into sections (which also works well with UIs):

```python
download_options = settings.Section("Downloader settings")
speed = settings.Number("Speed limit", 5, section=download_options)
dir = settings.Path("Target directory", '/home/yomama/Downloads', section=download_options)
server = settings.Choice("Mirror", ["Europe", "Asia", "America", "Africa"], "Asia", section=download_options)
```



## Did I mention free GUIs?

That's right, this library also includes a separate `settings_gui` package that has pre-made settings menus for both tkinter and ttk, with GTK and others to come. They have full integration with the aforementioned systems, like validation and sections.

Here's an example of some dummy settings with both libraries: 

*(notice the warning for the misspelt download path)*

![Ttk](https://github.com/SamuLumio/object-settings/blob/master/readme-images/ttk.png?raw=true)
*Nice-looking ttk (theme: Sun Valley dark)*

![Tkinter](https://github.com/SamuLumio/object-settings/blob/master/readme-images/tkinter.png?raw=true)
*Bare tkinter works too*

And you can get this automatically for all your defined settings by just calling one function (`SettingsFrame` or `SettingsWindow`, depending on preference)

Or, if you want to get more custom/contextual, you can also use the individual setting widgets and place them around your app (submodule `type_frames`).



## Setting types

List of currently available setting types:

- `Toggle`:
    A boolean True/False
- `Choice`:
    Choose an option (str) from a list
- `MappedChoice`:
    Choose an option (str) from a list, but have a different internal value mapped to it
- `Multichoice`:
    Choose multiple options (str) from a list
- `MappedMultichoice`:
    Choose multiple options (str) from a list, but have different internal values mapped to them
- `Text`:
    Just a basic text value
- `Path`:
    A file path whose existence can be checked
- `Number`:
    An integer that can be set or incremented and decremented

You can also inherit from the `BaseSetting` class to easily create custom ones.
