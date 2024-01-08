from defs_time import *

class license():
    def __init__(self, cuil: str, start: str, end: str, note: str):
        self.cuil = cuil
        self.start = f_check(start)
        self.end = f_check(end)
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