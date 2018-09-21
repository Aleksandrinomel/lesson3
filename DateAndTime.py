from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta

# Дата сегодня
print(date.today())
# Дата вчера
print(date.today() - timedelta(days=1))
# Дата месяц назад
print(date.today() - relativedelta(months=1))

date_string = '12/23/2010 12:10:03.234567'
date_dt = datetime.strptime(date_string, '%m/%d/%Y %H:%M:%S.%f')
print(date_dt)
