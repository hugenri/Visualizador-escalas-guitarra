from dataclasses import dataclass

@dataclass(frozen=True)
class Scale:
    id:str
    name:str
    intervals:tuple[int,...]
    def contains_interval(self,interval:int)->bool: return interval%12 in self.intervals
