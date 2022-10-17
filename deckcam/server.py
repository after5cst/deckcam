"""
The Bottle server used to handle incoming HTTP requests.
"""
import bottle
import requests
import threading
from .config import get_server_port
from .actions.press import Press
from .main import actions


def launch(*, server: bottle.ServerAdapter | None) -> threading.Thread:
    """
    Create the Bottle server and launch it on a thread.
    Returns the (started) thread object.
    """
    kwargs = dict(app=_create_bottle_app())

    if server is None:
        kwargs["port"] = get_server_port()
    else:
        kwargs["server"] = server

    th = threading.Thread(target=bottle.run, kwargs=kwargs)
    th.start()
    return th


def press(*, page: int, bank: int) -> None:
    result = requests.get(_url(f"/press/bank/{page}/{bank}"))
    result.raise_for_status()


def _url(suffix: str):
    return f"http://localhost:{get_server_port()}/{suffix}"


def _create_bottle_app() -> bottle.Bottle:
    app = bottle.Bottle()

    @app.route("/press/bank/<page>/<bank>")
    def press(page: int, bank: int) -> None:
        action = Press(page=page, bank=bank)
        actions.append(action.perform)

    return app
