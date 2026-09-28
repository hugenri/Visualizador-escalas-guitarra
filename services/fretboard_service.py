from dataclasses import dataclass
from domain.note import Note
from domain.scale import Scale
from domain.tuning import Tuning

@dataclass(frozen=True)
class FretNote:
    string_index:int
    fret:int
    note:Note
    interval:int
    is_root:bool

class FretboardService:

    def positions(self,tuning:Tuning,root:Note,scale:Scale,fret_count:int)->list[FretNote]:
        result=[]

        for string_index,open_note in enumerate(tuning.strings):
            for fret in range(fret_count+1):
                pitch=(open_note.pitch_class+fret)%12
                interval=(pitch-root.pitch_class)%12
                if scale.contains_interval(interval):
                    result.append(FretNote(string_index,fret,Note.from_pitch_class(pitch),interval,interval==0))
       
        return result
