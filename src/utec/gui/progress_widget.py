
import pytermgui as ptg
from apscheduler.schedulers.background import BaseScheduler

class ProgressWidget(ptg.Container):
    def __init__(self, **attrs) -> None:
        super().__init__(**attrs)
        self._n: int | float = 0
        self._total = 0
        self._desc = ""

    def _render(self) -> None:
        self.set_widgets([
            f"{self._n}/{self._total}",  # type: ignore
        ])

    def update(self, n: int | float | None=1, /) -> None:
        n = n if n is not None else 1
        self._n = min(self._n + n, self._total if self._total else 0)
        self._render()

    def set_description(self, desc: str) -> None:
        self._desc = desc
        self._render()

    def reset(self, total: float | None=...) -> None:
        self._total = total if total is not None else 0
        self._n = 0
        self._desc = ""
        self._render()

    @property
    def n(self) -> int | float: return self._n
        