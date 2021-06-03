import json
import os.path
import tkinter
from .settings import Settings

class SettingsEditor:
    @staticmethod
    def save (settings: Settings, *, file_path: str = "settings.json"):
        item_list = [dir_item for dir_item in dir (settings) if not (dir_item.startswith ("__") and dir_item.endswith ("__"))]
        items = {item: getattr (settings, item) for item in item_list}
        with open (file_path, "w") as out_file:
            json.dump (items, out_file)
    @staticmethod
    def load (*, file_path = "settings.json"):
        if os.path.exists (file_path):
            with open (file_path, "r") as in_file:
                settings_dict = json.load (in_file)
            return Settings (**settings_dict)
        else:
            settings = Settings ()
            SettingsEditor.save (settings = settings, file_path = file_path)
            return settings
    def edit (self, settings, after):
        self.settings = settings
        self.after = after
        self.main_window = tkinter.Toplevel ()
        self.header = tkinter.Label (self.main_window, text = "restart app after saving to apply changes")
        self.header.grid (row = 0, column = 0, columnspan = 2)
        self.item_list = [dir_item for dir_item in dir (settings) if not (dir_item.startswith ("__") and dir_item.endswith ("__"))]
        self.items = {item: getattr (settings, item) for item in self.item_list}
        self.getters = {}
        self.extra = {}
        item_index = 1
        for item_name, item in self.items.items ():
            label = tkinter.Label (self.main_window, text = item_name)
            label.grid (row = item_index, column = 0)
            if type (item) == bool:
                # print ("checkbox")
                variable = tkinter.IntVar ()
                variable.set (int (item))
                checkbox = tkinter.Checkbutton (self.main_window, variable = variable)
                checkbox.grid (row = item_index, column = 1)
                checkbox.select () if item else checkbox.deselect ()
                self.extra [item_name] = (variable, checkbox)
            elif type (item) in (str, int, float):
                # print ("text box")
                variable = tkinter.StringVar ()
                variable.set (str (item))
                text_box = tkinter.Entry (self.main_window, textvariable = variable)
                text_box.grid (row = item_index, column = 1)
                self.getters [item_name] = lambda: type (item) (variable.get ())
                self.extra [item_name] = (variable, text_box)
            else: raise Exception (f"setting editor doesn't implement type {type (item)}")

            item_index += 1
        save_button = tkinter.Button (self.main_window, text = "Save", command = self.post_edit)
        save_button.grid (row = item_index, column = 0, columnspan = 2)
    def post_edit (self):
        for item_name, item in self.items.items ():
            value = type (item) (self.extra [item_name] [0].get ())
            setattr (self.settings, item_name, value)
        self.main_window.destroy ()
        self.after ()