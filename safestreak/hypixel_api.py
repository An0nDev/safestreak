import functools

import requests

def make_req (*, endpoint: str, uuid: str, api_key: str):
    return requests.get (f"https://api.hypixel.net{endpoint}", params = {"key": api_key, "uuid": uuid}).json ()

def get_bedwars_stats (*, uuid: str, api_key: str):
    player_resp = make_req (endpoint = "/player", uuid = uuid, api_key = api_key)
    if not player_resp ["success"]:
        return False, player_resp ["cause"]
    else:
        if "Bedwars" in player_resp ["player"] ["stats"]:
            bw = player_resp ["player"] ["stats"] ["Bedwars"]
            return True, bw
        else:
            return True, {
                "Experience": 500,
                "final_kills_bedwars": 0,
                "final_deaths_bedwars": 0
            }

@functools.lru_cache (maxsize = None)
def get_player_uuid (*, username: str):
    response = requests.get (f"https://api.mojang.com/users/profiles/minecraft/{username}")
    response.raise_for_status ()
    if response.status_code == 204: return None
    return response.json () ["id"]