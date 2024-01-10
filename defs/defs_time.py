from datetime import datetime, timedelta


# return days
def proportion_oneyear(f: str):
    date = datetime.strptime(f, r'%Y-%m-%d')
    months = 13 - date.month
    days = (months * 20) // 12
    return days

# return days
def days_of_licence(years: int):
    if years <= 5:
        return 20
    elif years <= 10:
        return 25
    elif years <= 15:
        return 30
    else:
        return 35

# return years
def years_of_work(f: str):
    date = datetime.strptime(f, r'%Y-%m-%d')
    today = datetime.now()
    dif = today - date
    return dif.days // 365

#  6 = sunday
def Weekend_check(f: str):
    date = datetime.strptime(f, r'%Y-%m-%d')
    week_day = date.weekday()
    if week_day == 6:
        return date.strftime(r'%Y-%m-%d')
    else:
        raise ValueError('La fecha del fin de la licencia no es Domingo')

# return str or Error
def f_check(f: str):
    formats = [r'%d/%m/%Y', r'%d-%m-%Y', r'%d.%m.%Y', r'%Y-%m-%d']
    for date_format in formats:
        try:
            date = datetime.strptime(f, date_format)
            return date.strftime(r'%Y-%m-%d')  # Normalizar la fecha al formato 'YYYY-MM-DD'
        except ValueError:
            pass
    raise ValueError("Fecha no válida")



# return str
def days_between(f1: str, f2: str):
    date_1 = datetime.strptime(f1, r'%Y-%m-%d')
    date_2 = datetime.strptime(f2, r'%Y-%m-%d')
    dif = date_2 - date_1
    days = dif.days
    return days + 1

# return dict
def days_origin(admission: str, years: list, to_list: bool = False):
    date = datetime.strptime(admission, r'%Y-%m-%d')
    days_per_years_dict= dict()
    days_per_years_list= list()
    for year in years:
        if date.year > year:
            days = 0
        elif date.year == year:
            days = proportion_oneyear(admission)
        else:
            days = days_of_licence(years_of_work(admission))
        days_per_years_dict[f'{str(year)}-12-01'] = days
        days_per_years_list.append([f'{str(year)}-12-01', days])
    if to_list:
        return days_per_years_list
    return days_per_years_dict

 # return list of str
def orderby_date(dates: list):
    try:
        date_objects = [datetime.strptime(date, r'%Y-%m-%d') for date in dates]
    except ValueError:
        print('incorrect dates')
    sorted_dates_objects = sorted(date_objects)
    sorted_dates = []
    for date in sorted_dates_objects:
        sorted_dates.append(date.strftime(r'%Y-%m-%d'))
    return sorted_dates

# return bool
def is_less(f1, f2):
    date_1 = datetime.strptime(f1, r'%Y-%m-%d')
    date_2 = datetime.strptime(f2, r'%Y-%m-%d')
    if date_1  < date_2:
        return True
    else:
        return False

# return str
def add_years(f, years: int):
    date = datetime.strptime(f, r'%Y-%m-%d')
    new_date = date + timedelta(days=365 * years)
    return new_date.strftime(r'%Y-%m-%d')