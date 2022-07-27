import json
import os.path
import time
import threading

from .hypixel_api import APIException, get_player_uuid, get_bedwars_stats
from .bedwars_calcs import xp_to_level

class StatsFetchFailureException(Exception):
    def __init__(self):
        super().__init__("Couldn't fetch stats")

class StatsFetcher:
    def __init__ (self, app):
        self.app = app
        self.stats_cache_file_full_path = self.app.data_path / self.app.settings.stats_cache_file_path
        if os.path.exists (self.stats_cache_file_full_path):
            with open (self.stats_cache_file_full_path, "r") as cache_file:
                try:
                    self.cache = json.load (cache_file)
                except json.decoder.JSONDecodeError:
                    self._make_empty_cache()
        else:
            self._make_empty_cache()
        self.uuid_yoink_lock = threading.Lock ()
    def _make_empty_cache(self):
        self.cache = {}
        with open (self.stats_cache_file_full_path, "w+") as cache_file: json.dump (self.cache, cache_file)
    def fetch_for (self, *, username: str) -> (dict, str):
        with self.uuid_yoink_lock:
            uuid = get_player_uuid (username = username)
            if uuid is None: return None, None

            if (uuid in self.cache) and (time.time () < (self.cache [uuid] ["at"] + self.app.settings.stats_cache_max_time_seconds)):
                return self.cache [uuid] ["stats"], uuid

        try:
            og_stats = get_bedwars_stats (uuid = uuid, api_key = self.app.settings.hypixel_api_key)
        except APIException:
            raise StatsFetchFailureException()
        if og_stats is None: return None, None
        star = xp_to_level (xp = og_stats ["Experience"] if "Experience" in og_stats else 0)
        final_kills = og_stats ["final_kills_bedwars"] if "final_kills_bedwars" in og_stats else 0
        final_deaths = og_stats ["final_deaths_bedwars"] if "final_deaths_bedwars" in og_stats else 0
        stats = {
            "star": star,
            "fkdr": (final_kills / final_deaths) if final_deaths > 0 else 0,
        }
        with self.uuid_yoink_lock:
            self.cache [uuid] = {
                "at": time.time (),
                "stats": stats
            }
            with open (self.stats_cache_file_full_path, "w") as cache_file: json.dump (self.cache, cache_file)
        return stats, uuid
