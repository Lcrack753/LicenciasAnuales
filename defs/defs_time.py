from datetime import datetime


# return days
def proportion_oneyear(f: str):
    date = datetime.strptime(f, r'%d/%m/%Y')
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
    date = datetime.strptime(f, r'%d/%m/%Y')
    today = datetime.now()
    dif = today - date
    return dif.days // 365

# return 5 = saturday / 6 = sunday
def Weekend_check(f: str):
    date = datetime.strptime(f, r'%d/%m/%Y')
    week_day = date.weekday()
    if week_day == 5 or week_day == 6:
        return week_day
    else:
        return False

# return boolean
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
    return days