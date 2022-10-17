import pathlib
import configparser

_THIS_DIR = pathlib.Path(__file__).parent


def _get_ini() -> pathlib.Path:

    config = configparser.ConfigParser()
    config.read(_THIS_DIR / "deckcam.ini")
    return config["deckcam"]


def get_server_port() -> int:
    return _get_ini()["server_port"]
