import dataclasses

@dataclasses.dataclass
class Settings:
    always_on_top: bool = True
    transparency: float = 0.5
    font_name: str = "Arial"
    font_size: int = 12
    scale: float = 1
    own_ign: str = "An0nDev"
    hypixel_api_key: str = "1c5aa45c-6dfb-43da-8296-1f454e3f201b"
    stats_cache_file_path: str = "stats_cache.json"
    stats_cache_max_time_seconds: float = 60 * 60 * 24
    fkdr_digits: int = 2
    index_score_constant_scale: float = 20
    index_score_digits: int = 2
    star_divisor: int = 30
    fkdr_power: float = 2.0
    multiply_star_by_fkdr: bool = False
