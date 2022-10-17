import bottle
import socket

import deckcam.config
import deckcam.main
import deckcam.server
from deckcam.actions.press import Press


class SingleCommandServer(bottle.ServerAdapter):
    def __init__(self):
        host, port = deckcam.config.get_server()
        bottle.ServerAdapter.__init__(self, host=host, port=port)

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


def test_incoming_press_is_put_in_queue():
    server_thread = deckcam.server.launch(server=SingleCommandServer())
    deckcam.server.press(page=1, bank=1)
    server_thread.join()
    assert 1 == len(deckcam.main.actions)
    action = deckcam.main.actions.popleft()
    assert isinstance(action, Press)


def test_foo():
    from deckcam.actions.press import HighlightStreamDeckSelection

    for bank in range(1, 9):
        HighlightStreamDeckSelection(page=1, bank=bank)()

    assert False, """NEXT STEPS: Make CSVs to define behavior:
    "Name", "Preset", "Cam1Random", "Cam2Random", "Cam3Random",
    "Pulpit", 0, False, False, False,
    "Carissa", 1, True, True, False,
    ...
    """
