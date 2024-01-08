from defs_time import *

class license():
    def __init__(self, cuil: str, start: str, end: str, note: str):
        self.cuil = cuil
        self.start = f_check(start)
        self.end = Weekend_check(f_check(end))
        self.days_btw = days_between(self.start, self.end)
        self.note = note
    
    def to_dict(self):
        z = {
            'cuil': self.cuil,
            'start': self.start,
            'end': self.end,
            'days_btw': self.days_btw,
            'note': self.note
        }
        return z


class agent():
    def __init__(self, cuil: str, first: str, last: str, admission: str):
        self.cuil = cuil
        self.first = first
        self.last = last
        self.admission = f_check(admission)
        self.days_origin = days_origin(self.admission, range(2021,2027))
    
    def to_dict(self):
        z = {
            'cuil': self.cuil,
            'first': self.first,
            'last': self.last,
            'admission': self.admission,
        }
        z.update(self.days_origin)
        return z