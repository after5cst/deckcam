import pathlib
import configparser
from typing import Tuple

_THIS_DIR = pathlib.Path(__file__).parent


def _get_ini() -> pathlib.Path:

    config = configparser.ConfigParser()
    config.read(_THIS_DIR / "deckcam.ini")
    return config["deckcam"]


def get_host() -> str:
    return "127.0.0.1"


def get_server() -> Tuple[str, int]:
    return (get_host(), int(_get_ini()["server_port"]))


def get_streamdeck_udp() -> Tuple[str, int]:
    return (get_host(), int(_get_ini()["streamdeck_udp"]))
