from . import Action


class Press:
    def __init__(self, *, page: int, bank: int) -> None:
        self.page = page
        self.bank = bank

    def perform(self) -> list[Action]:
        # TODO
        return []
