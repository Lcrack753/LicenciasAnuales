from defs.defs_time import *

class vacation():
    def __init__(self, cuil: str, start: str, end: str, note: str):
        if not f_check(start) or not f_check(end):
            raise ValueError("Las fechas proporcionadas no son válidas.")
        self.cuil = cuil
        self.start = start
        self.end = end
        self.days_btw = days_between(self.start, self.end)
        self.note = note
    
    def to_dict(self):
        v = {
            'cuil': self.cuil,
            'start': self.start,
            'end': self.end,
            'days_btw': self.days_btw,
            'note': self.note
        }
        return v
    
    