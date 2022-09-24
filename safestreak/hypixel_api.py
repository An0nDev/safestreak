import functools
import typing

import requests

class APIException(Exception):
    def __init__(self, cause: str, resp_code: int):
        super().__init__(cause)
        self.resp_code = resp_code

INVALID_API_KEY_CAUSE = "Invalid API key"
INVALID_API_KEY_RESP_CODE = 403
class InvalidAPIKeyException(APIException):
    def __init__(self):
        super().__init__(INVALID_API_KEY_CAUSE, INVALID_API_KEY_RESP_CODE)

def make_req (*, api_key: str, endpoint: str, **kwargs):
    resp = requests.get (f"https://api.hypixel.net{endpoint}", params = {"key": api_key} | kwargs)
    resp_json = resp.json()

    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        cause = resp_json["cause"]
        resp_code = resp.status_code

        if cause == INVALID_API_KEY_CAUSE and resp_code == INVALID_API_KEY_RESP_CODE:
            raise InvalidAPIKeyException()
        else:
            raise APIException(cause, resp_code)

    assert resp_json["success"]
    del resp_json["success"]
    return resp_json


def test(*, api_key: typing.Optional[str]) -> str:
    if api_key is None:
        raise InvalidAPIKeyException()
    resp = make_req(api_key=api_key, endpoint="/key")
    return get_player_username(uuid=resp["record"]["owner"])


def get_bedwars_stats (*, api_key: str, uuid: str) -> typing.Optional[dict]:
    player_resp = make_req (api_key = api_key, endpoint = "/player", uuid = uuid)
    if player_resp ["player"] is None: return None
    if "Bedwars" in player_resp ["player"] ["stats"]:
        bw = player_resp ["player"] ["stats"] ["Bedwars"]
        return bw
    else:
        return {
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

@functools.lru_cache(maxsize=None)
def get_player_username(*, uuid: str):
    response = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")
    response.raise_for_status()
    return response.json()["name"]
