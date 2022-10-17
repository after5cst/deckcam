# from typing import Protocol


# class Action(Protocol):
#     def perform(self) -> list["Action"]:
#         ...
from typing import Callable

Action = Callable[[], "Action"]
