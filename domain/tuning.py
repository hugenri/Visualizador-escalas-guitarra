from dataclasses import dataclass
from .note import Note

@dataclass(frozen=True)
class Tuning:
    id:str
    name:str
    strings:tuple[Note,...]

STANDARD_TUNING=Tuning("standard","Standard (E A D G B E)",tuple(Note.from_name(n) for n in ("E","A","D","G","B","E")))
