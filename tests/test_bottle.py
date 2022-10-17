import bottle
import requests
import socket
import threading
from typing import Any

import deckcam.config
import deckcam.main
import deckcam.server
from deckcam.actions.press import Press


class SingleCommandServer(bottle.ServerAdapter):
    def __init__(self, host="127.0.0.1", port=None, **options):
        if port is None:
            port = deckcam.config.get_server_port()
        bottle.ServerAdapter.__init__(self, host=host, port=port, **options)

    def run(self, app):  # pragma: no cover
        from wsgiref.simple_server import WSGIRequestHandler, WSGIServer
        from wsgiref.simple_server import make_server

        class FixedHandler(WSGIRequestHandler):
            def address_string(self):  # Prevent reverse DNS lookups please.
                return self.client_address[0]

            def log_request(*args, **kw):
                if not self.quiet:
                    return WSGIRequestHandler.log_request(*args, **kw)

        handler_cls = self.options.get("handler_class", FixedHandler)
        server_cls = self.options.get("server_class", WSGIServer)

        if ":" in self.host:  # Fix wsgiref for IPv6 addresses.
            if getattr(server_cls, "address_family") == socket.AF_INET:

                class server_cls(server_cls):
                    address_family = socket.AF_INET6

        srv = make_server(self.host, self.port, app, server_cls, handler_cls)
        srv.handle_request()


# def make_call_with_bottle(command: callable, *args, **kwargs) -> Any:
#     app = bottle.Bottle()
#     server = SingleCommandServer()

#     @app.route("/")
#     def endpoint():
#         command(*args, **kwargs)

#     th = threading.Thread(target=bottle.run, kwargs=dict(app=app, server=server))
#     th.start()

#     result = requests.get(f"http://{server.host}:{server.port}/")
#     assert result.ok

#     th.join()
#     return result


# def test_can_route_via_bottle():
#     class MyObject:
#         def __init__(self):
#             self.called = False

#         def callback(self) -> None:
#             self.called = True

#     obj = MyObject()
#     make_call_with_bottle(obj.callback)
#     assert obj.called


def test_incoming_press_is_put_in_queue():
    server_thread = deckcam.server.launch(server=SingleCommandServer())
    deckcam.server.press(page=1, bank=1)
    server_thread.join()
    assert 1 == len(deckcam.main.actions)
    action = deckcam.main.actions.popleft()
    assert 0 == len(action())  # TODO : will break once Press creates more objects.
