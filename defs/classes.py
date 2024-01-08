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

class days_available():
    def __init__(self, license: list, agent: tuple):       
        self.days_of = [{'date': row[0], 'days': row[1]} for row in license]
        self.days_of = sorted(self.days_of, key=lambda x: x['date'])

        self.years = range(2021,2027)
        self.agent_days = [{f'year_{str(year)}': value} for value, year in zip(agent, self.years)]

        self.days_left = self.days_of.copy()
        
    def take_days(self):
            pass
    
days_available([('2023-06-05', 15), ('2023-11-14', 15), ('2020-02-06', 5)],(0,0,0,8,0,0,0))