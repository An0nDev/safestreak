import math
import os
import tkinter
import pathlib

from .chat_processor import ChatProcessor
from .log_reader import LogReader
from .settings import Settings
from .stats_fetcher import StatsFetcher
from .ui import Controls, Container
from .settings_editor import SettingsEditor

class safestreakApp (tkinter.Tk):
    def __init__ (self):
        super ().__init__ ()

        self.data_path = pathlib.Path.home () / ".safestreak"
        if not os.path.exists (self.data_path): os.mkdir (self.data_path)
        self.settings_path = self.data_path / "settings.json"
        self.settings = SettingsEditor.load (file_path = self.settings_path)

        if self.settings.always_on_top: self.attributes ("-topmost", True)
        self.wait_visibility (self)
        self.wm_attributes ("-alpha", self.settings.transparency)
        self.configure (bg = "black")
        self.wm_title ("safestreak")

        self.top_text = tkinter.Label (self, text = "TOP TEXT", bg = "black", fg = "white", font = ("Impact", 36))
        self.top_text.grid (row = 0, sticky = "we")

        self.title_text = tkinter.Label (self, text = "safestreak by an0ndev; gl and enjoy <3", **self.gen_global_widget_opts (bigger_text = True))
        self.title_text.grid (row = 1, sticky = "we")

        self.stats_fetcher = StatsFetcher (self)
        self.chat_processor = ChatProcessor (self)
        self.log_reader = LogReader (self)

        self.container = Container (self)
        self.controls = Controls (self)
        self.controls.grid (row = 2, sticky = "we")
        self.container.grid (row = 3, sticky = "we")
        self.container.add_row (self.settings.own_ign, pinned = True)

        self.bottom_text = tkinter.Label (self, text = "BOTTOM TEXT", bg = "black", fg = "white", font = ("Impact", 36))
        self.bottom_text.grid (row = 4, sticky = "we")
    def gen_global_widget_opts (self, is_container = False, bigger_text = False):
        opts = {"bg": "black"}
        if not is_container: opts = {**opts, "fg": "white", "font": (self.settings.font_name, math.floor (self.settings.font_size * (1.5 if bigger_text else 1) * self.settings.scale))}
        return opts
    def calc_index_score (self, stats):
        return ((stats ["star"] / 100) + (stats ["fkdr"] ** 2)) * self.settings.index_score_constant_scale
    COOL_PEOPLE_LIST = ["d9f9d8ea4f054a5fac211b51d9e448ad", "3712b4872b2346c38d6774fa3d27b58f", "518d492516a447b4a56213d5465f0eba", "06b57734e6eb4ee3a7b53492d5fbb5e6"]