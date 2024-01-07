from datetime import datetime



def proportion_oneyear(f: str):
    date = datetime.strptime(f, r'%d/%m/%Y')
    months = 13 - date.month
    days = (months * 20) // 12
    return days


def days_of_licence(years: int):
    if years <= 5:
        return 20
    elif years <= 10:
        return 25
    elif years <= 15:
        return 30
    else:
        return 35


def years_of_work(f: str):
    date = datetime.strptime(f, r'%d/%m/%Y')
    today = datetime.now()
    dif = today - date
    return dif.days // 365


def Weekend_check(f: str):
    date = datetime.strptime(f, r'%d/%m/%Y')
    week_day = date.weekday()
    if week_day == 5 or week_day == 6:
        return week_day
    else:
        return False


def f_check(f: str):
    try:
        datetime.strptime(f, r'%d/%m/%Y')
        print('Fecha Valida')
        return True
    except ValueError:
        print('Fecha No Valida')
        return False


def dates_between(f1: str, f2: str):
    date_1 = datetime.strptime(f1, r'%d/%m/%Y')
    date_2 = datetime.strptime(f2, r'%d/%m/%Y')
    dif = date_2 - date_1
    days = dif.days
    return days




print(years_of_work('4/01/2020'))
