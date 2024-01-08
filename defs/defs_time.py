from datetime import datetime


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


def f_check(f: str):
    formats = [r'%d/%m/%Y', r'%d-%m-%Y', r'%d.%m.%Y', r'%Y-%m-%d']
    for date_format in formats:
        try:
            date = datetime.strptime(f, date_format)
            return date.strftime(r'%Y-%m-%d')  # Normalizar la fecha al formato 'YYYY-MM-DD'
        except ValueError:
            pass
    raise ValueError("Fecha no válida")



# return string
def days_between(f1: str, f2: str):
    date_1 = datetime.strptime(f1, r'%Y-%m-%d')
    date_2 = datetime.strptime(f2, r'%Y-%m-%d')
    dif = date_2 - date_1
    days = dif.days
    return days + 1

# return dict
def days_origin(admission: str, years: list):
    date = datetime.strptime(admission, r'%Y-%m-%d')
    days_per_years= dict()
    for year in years:
        if date.year > year:
            days = 0
        elif date.year == year:
            days = proportion_oneyear(admission)
        else:
            days = days_of_licence(years_of_work(admission))
        days_per_years[f'year_{year}'] = days
    return days_per_years

def orderby_date(dates: list):
    try:
        date_objects = [datetime.strptime(date, r'%Y-%m-%d') for date in dates]
    except ValueError:
        print('incorrect dates')
    sorted_dates_objects = sorted(date_objects)
    sorted_dates = []
    for date in sorted_dates_objects:
        sorted_dates.append(f'{date.year}-{date.month}-{date.day}')
    return sorted_dates
