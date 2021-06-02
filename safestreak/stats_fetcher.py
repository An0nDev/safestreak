import json
import os.path
import time

from .hypixel_api import get_player_uuid, get_bedwars_stats
from .bedwars_calcs import xp_to_level

class StatsFetcher:
    def __init__ (self, app):
        self.app = app
        self.stats_cache_file_full_path = self.app.data_path / self.app.settings.stats_cache_file_path
        if os.path.exists (self.stats_cache_file_full_path):
            with open (self.stats_cache_file_full_path, "r") as cache_file: self.cache = json.load (cache_file)
        else:
            self.cache = {}
            with open (self.stats_cache_file_full_path, "w+") as cache_file: json.dump (self.cache, cache_file)
    def fetch_for (self, *, username: str):
        uuid = get_player_uuid (username = username)
        if uuid is None: return None, None

        if (uuid in self.cache) and (time.time () < (self.cache [uuid] ["at"] + self.app.settings.stats_cache_max_time_seconds)):
            return self.cache [uuid] ["stats"], uuid

        success, og_stats = get_bedwars_stats (uuid = uuid, api_key = self.app.settings.hypixel_api_key)
        if not success: raise Exception (f"couldn't get stats: {og_stats}")
        star = xp_to_level (xp = og_stats ["Experience"] if "Experience" in og_stats else 0)
        final_kills = og_stats ["final_kills_bedwars"] if "final_kills_bedwars" in og_stats else 0
        final_deaths = og_stats ["final_deaths_bedwars"] if "final_deaths_bedwars" in og_stats else 0
        stats = {
            "star": star,
            "fkdr": (final_kills / final_deaths) if final_deaths > 0 else 0,
        }
        self.cache [uuid] = {
            "at": time.time (),
            "stats": stats
        }
        with open (self.stats_cache_file_full_path, "w") as cache_file: json.dump (self.cache, cache_file)
        return stats, uuid