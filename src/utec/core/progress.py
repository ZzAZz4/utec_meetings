from typing import Protocol, Any
from tqdm import tqdm


class ProgressIndicator(Protocol):
    def update(self, value: int | float | None=..., /) -> Any: ...
    def set_description(self, desc: str): ...
    def reset(self, total: float | None=...): ...
    @property
    def n(self) -> int | float: ...
    

class EmptyProgressIndicator:
    def update(self, value: int | float | None=..., /) -> None: pass
    def set_description(self, desc: str): pass
    def reset(self, total: float | None=...): pass
    @property
    def n(self): return 0

t: ProgressIndicator = tqdm()
t.reset()