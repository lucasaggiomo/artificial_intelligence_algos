from typing import TypeVar

from src.agentPackage.action import Action
from src.agentPackage.state import State

# TypeVar per i tipi generici
S = TypeVar("S", bound=State)
A = TypeVar("A", bound=Action)
