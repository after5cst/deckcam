from . import Action
from ..config import get_streamdeck_udp
import socket

_STREAMDECK_ROW_SIZE = 8


# TODO: move to another file.
class HighlightStreamDeckSelection:
    def __init__(self, *, page: int, bank: int) -> None:
        self.page = int(page)
        self.bank = int(bank)
        self.host, self.port = get_streamdeck_udp()

    def _send(self, MESSAGE: str) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP
        sock.sendto(MESSAGE.encode(), (self.host, self.port))

    def __call__(self) -> list[Action]:
        row = (self.bank - 1) // _STREAMDECK_ROW_SIZE
        begin = row * _STREAMDECK_ROW_SIZE + 1
        end = begin + _STREAMDECK_ROW_SIZE

        for bank in range(begin, end):
            bgcolor = "ffd700" if bank == self.bank else "000000"
            message = f"STYLE BANK {self.page} {bank} BGCOLOR {bgcolor}"
            self._send(message)

            color = "000000" if bank == self.bank else "f5f5f5"
            message = f"STYLE BANK {self.page} {bank} COLOR {color}"
            self._send(message)
        return []


class Press:
    def __init__(self, *, page: int, bank: int) -> None:
        self.page = int(page)
        self.bank = int(bank)

    def __call__(self) -> list[Action]:
        return [
            HighlightStreamDeckSelection(page=self.page, bank=self.bank),
        ]
