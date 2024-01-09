from defs_time import *

class license():
    def __init__(self, cuil: str, start: str, end: str, note: str):
        self.cuil = cuil
        self.start = f_check(start)
        self.end = f_check(end)
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
        self.days_origin_dict = days_origin(self.admission, range(2021,2027)) # Dynamic years
        self.days_origin_tuple = tuple((self.days_origin_dict[date] for date in self.days_origin_dict.keys()))

    def to_dict(self):
        z = {
            'cuil': self.cuil,
            'first': self.first,
            'last': self.last,
            'admission': self.admission,
        }
        return z
    
    def days_available(self,licenses: list):
        self.licenses = licenses
        self.licenses = sorted(self.licenses, key=lambda x: x[0])
        

    
class days_available():
    def __init__(self, license: list, agent: tuple): # fetch_license(reduce=True) ; agent.days_origin_to_tuple()      
        # self.days_of = [[row[0], row[1]] for row in license]
        self.days_of = license
        self.days_of = sorted(self.days_of, key=lambda x: x[0])
        
        self.years = [2021+i for i in range(0,len(agent))]
        self.agent_days = [[f'{str(year)}-12-01', value] for value, year in zip(agent, self.years)]

        self.days_taken = self.days_of.copy()
        self.days_left = self.agent_days.copy()
        self.take_days()
    
    def take_days(self):
        for i in range(0, len(self.days_left)):
            for j in range(0, len(self.days_taken)):
                if is_less(self.days_taken[j][0],self.days_left[i][0]):
                    continue
                elif not is_less(self.days_taken[j][0],add_years(self.days_left[i][0], 2)):
                    continue
                
                while True:
                    if self.days_taken[j][1] == 0 or self.days_left[i][1] == 0:
                        break
                    self.days_taken[j][1] -= 1
                    self.days_left[i][1] -= 1

    def to_dict(self):
        z = {}
        for date in self.days_left:
            year = date[0].split('-')[0]
            z.update({f'year_{year}':date[1]})
        return z
