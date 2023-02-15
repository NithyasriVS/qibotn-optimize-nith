from dataclasses import dataclass
from typing import Optional


@dataclass
class Executor:
    backend: str
    platform: Optional[str] = None
    swaps: bool = True


qibo = Executor(backend="qibojit", platform="numpy")
quimb = Executor(backend="numpy")
