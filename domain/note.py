from dataclasses import dataclass

NOTE_NAMES_SHARP=("C","C#","D","D#","E","F","F#","G","G#","A","A#","B")
NOTE_NAMES_FLAT=("C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B")
NOTE_TO_SEMITONE={"C":0,"B#":0,"C#":1,"Db":1,"D":2,"D#":3,"Eb":3,"E":4,"Fb":4,"F":5,"E#":5,"F#":6,"Gb":6,"G":7,"G#":8,"Ab":8,"A":9,"A#":10,"Bb":10,"B":11,"Cb":11}

@dataclass(frozen=True)
class Note:
    name:str
    pitch_class:int
    @staticmethod
    def from_name(name:str)->"Note":
        if name not in NOTE_TO_SEMITONE: raise ValueError(f"Nota no válida: {name}")
        return Note(name,NOTE_TO_SEMITONE[name])
    @staticmethod
    def from_pitch_class(pitch_class:int,prefer_flats:bool=False)->"Note":
        names=NOTE_NAMES_FLAT if prefer_flats else NOTE_NAMES_SHARP
        return Note(names[pitch_class%12],pitch_class%12)
