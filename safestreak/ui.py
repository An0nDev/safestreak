import copy
import math
import tkinter
from .settings_editor import SettingsEditor

class Controls (tkinter.Frame):
    def __init__ (self, master):
        self.app = master
        super ().__init__ (master, **self.app.gen_global_widget_opts (is_container = True))
        self.settings_button = tkinter.Button (self, text = "Settings", command = self._edit_settings, **self.app.gen_global_widget_opts ())
        self.settings_button.grid (row = 0, column = 1, sticky = "NS")
        self.clear_button = tkinter.Button (self, text = "Clear", command = self.app.container.clear_rows, **self.app.gen_global_widget_opts ())
        self.clear_button.grid (row = 0, column = 2, sticky = "NS")
        self.app.bind ("<Escape>", lambda event: self.app.container.clear_rows ())
        self.custom_field_value = tkinter.StringVar ()
        self.custom_field = tkinter.Entry (self, textvariable = self.custom_field_value, **self.app.gen_global_widget_opts ())
        self.custom_field.bind ("<Return>", lambda event: self._add ())
        self.custom_field.grid (row = 0, column = 3, sticky = "NS")
        self.custom_add_button = tkinter.Button (self, text = "Add", command = self._add, **self.app.gen_global_widget_opts ())
        self.custom_add_button.grid (row = 0, column = 4, sticky = "NS")
    def _edit_settings (self):
        SettingsEditor ().edit (self.app.settings, after = self._edit_settings_after)
    def _edit_settings_after (self):
        SettingsEditor.save (self.app.settings, file_path = self.app.settings_path)
    def _add (self):
        with self.app.container_lock:
            self.app.container.add_row (self.custom_field_value.get (), pinned = False)
        self.custom_field_value.set ("")

class Container (tkinter.Frame):
    def __init__ (self, master):
        self.app = master
        super ().__init__ (master, **self.app.gen_global_widget_opts (is_container = True))

        username_label = tkinter.Label (self, text = "USERNAME", **self.app.gen_global_widget_opts ())
        username_label.grid (row = 0, column = 0)
        star_label = tkinter.Label (self, text = "STAR", **self.app.gen_global_widget_opts ())
        star_label.grid (row = 0, column = 1)
        fkdr_label = tkinter.Label (self, text = "FKDR", **self.app.gen_global_widget_opts ())
        fkdr_label.grid (row = 0, column = 2)
        index_label = tkinter.Label (self, text = "INDEX", **self.app.gen_global_widget_opts ())
        index_label.grid (row = 0, column = 3)
        pin_label = tkinter.Label (self, text = "PIN", **self.app.gen_global_widget_opts ())
        pin_label.grid (row = 0, column = 4)
        remove_label = tkinter.Label (self, text = "DEL", **self.app.gen_global_widget_opts ())
        remove_label.grid (row = 0, column = 5)
        self.label_row = [username_label, star_label, fkdr_label, index_label, pin_label, remove_label]

        self.rows = {}
    def add_row (self, username: str, pinned: bool = False):
        if username in self.rows:
            row = self.rows [username]
            if not row ["pinned"] and pinned:
                row ["pinned"] = True
                row ["columns"] [4].configure (text = "U")
            return
        row_index = len (self.rows) + 1

        username_col = tkinter.Label (self, text = username, **self.app.gen_global_widget_opts ())
        username_col.grid (row = row_index, column = 0)
        stats, uuid = self.app.stats_fetcher.fetch_for (username = username)
        is_nick = stats is None
        text_opts = self.app.gen_global_widget_opts ()
        if uuid in self.app.COOL_PEOPLE_LIST:
            text_opts ["fg"] = "gold2"
            username_col.configure (fg = "gold2")
        if is_nick:
            text_opts ["fg"] = "firebrick1"
            username_col.configure (fg = "firebrick1")
        star_col = tkinter.Label (self, text = f"{math.floor (stats ['star'])}✫" if not is_nick else "WARN", **text_opts)
        star_col.grid (row = row_index, column = 1)
        fkdr_col = tkinter.Label (self, text = f"{str (round (stats ['fkdr'], self.app.settings.fkdr_digits)).zfill (self.app.settings.fkdr_digits)}fkdr" if not is_nick else "NICK", **text_opts)
        fkdr_col.grid (row = row_index, column = 2)
        index_score = round (self.app.calc_index_score (stats), self.app.settings.index_score_digits) if not is_nick else 999
        index_col = tkinter.Label (self, text = f"{str (index_score).zfill (self.app.settings.index_score_digits)}I" if not is_nick else "UNK", **text_opts)
        index_col.grid (row = row_index, column = 3)
        pinned_toggle_col = tkinter.Button (self, text = "U" if pinned else "P", command = lambda: self.toggle_pin (username), **self.app.gen_global_widget_opts ())
        pinned_toggle_col.grid (row = row_index, column = 4)
        remove_button_col = tkinter.Button (self, text = "X", command = lambda: self.remove_row (username, force = True), **self.app.gen_global_widget_opts ())
        remove_button_col.grid (row = row_index, column = 5)

        self.rows [username] = {"columns": [username_col, star_col, fkdr_col, index_col, pinned_toggle_col, remove_button_col], "index": row_index, "index_score": index_score, "pinned": pinned}

        sorted_rows = sorted (self.rows.items (), key = lambda username_and_row: username_and_row [1] ["index_score"], reverse = True)
        self._reindex (sorted_rows)
    @staticmethod
    def _reindex (items):
        new_row_index = 1
        for username, row in items:
            row ["index"] = copy.deepcopy (new_row_index)
            column_index = 0
            for column in row ["columns"]:
                column.grid_forget ()
                column.grid (row = new_row_index, column = column_index)
                column_index += 1
            new_row_index += 1
    def toggle_pin (self, username):
        row = self.rows [username]
        row ["pinned"] = not row ["pinned"]
        row ["columns"] [4].configure (text = "U" if row ["pinned"] else "P")
    def remove_row (self, username, force = False):
        if username not in self.rows: return
        row = self.rows [username]
        if row ["pinned"] and not force: return
        for column in row ["columns"]:
            column.grid_forget ()
        del self.rows [username]

        sorted_rows = sorted (self.rows.items (), key = lambda username_and_row: username_and_row [1] ["index_score"], reverse = True)
        self._reindex (sorted_rows)
    def clear_rows (self, force = False):
        pins = []
        for username in list (self.rows.keys ()):
            if (not force) and self.rows [username] ["pinned"]: pins.append (username)
            self.remove_row (username)
        if not force:
            for pinned in pins: self.add_row (pinned, pinned = True)
