from datetime import date
from datetime import datetime

TODAY_STR = str(date.today())


def preclean(raw_date_string_fscope):
    if 'hour' in raw_date_string_fscope:
        # today
        # 'Posted 2 hours ago'
        return TODAY_STR
    else:
        # 'Posted on 2-Dec-22'
        date_string = raw_date_string_fscope.removeprefix('Posted on ')
        return date_string


def check_alphabet(date_string):
    for letter in date_string:
        if letter.isalpha():
            return True    #contains month
    return False


def date_reformat(raw_date_string):
    date_string = preclean(raw_date_string)
    if check_alphabet(date_string):
        # alphabet in string means there are months
        odate = datetime.strptime(date_string, '%d-%b-%y')
    else:
        odate = datetime.strptime(date_string, '%Y-%m-%d')
    date_reformatted = odate.strftime('%Y-%m-%d')
    return date_reformatted


