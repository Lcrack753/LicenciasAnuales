from defs_time import *
import copy
import os

class License():
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


class Agent():
    def __init__(self, cuil: str, first: str, last: str, admission: str, area: str):
        self.years = range(2021,2025) # Dynamic years
        self.cuil = cuil
        self.first = first
        self.last = last
        self.admission = f_check(admission)
        self.area = area
        self.days_origin_dict = days_origin(self.admission, self.years)
        self.days_origin_list = days_origin(self.admission, self.years, to_list=True)


    def to_dict(self):
        z = {
            'cuil': self.cuil,
            'first': self.first,
            'last': self.last,
            'admission': self.admission,
            'area': self.area
        }
        return z
    
    def days_available(self,licenses_list: list, to_dict: bool = False):
        # licenses -> [[date_1,days_1], [date_2,days_2], [date_n,days_n]] [['2022-05-23',15],['2023-08-01',5]]
        licenses = sorted(licenses_list, key=lambda x: x[0])
        days_origin_list_copy = copy.deepcopy(self.days_origin_list)
        for origin_index, origin in enumerate(days_origin_list_copy):
            for license_index, license in enumerate(licenses):
                if is_less(license[0], origin[0]):
                    continue
                elif not is_less(license[0],add_years(origin[0], 2)):
                    continue
                while True:
                    if days_origin_list_copy[origin_index][1] == 0 or licenses[license_index][1] == 0:
                        break
                    licenses[license_index][1] -= 1
                    days_origin_list_copy[origin_index][1] -= 1
        if not to_dict:
            return days_origin_list_copy
        return dict((x[0], x[1]) for x in days_origin_list_copy)

