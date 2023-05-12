import datetime
date = '2021-05-21 11:22:03'
datem = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
print(datem.day)        # 25
print(datem.month)      # 5
print(datem.year)       # 2021
print(datem.hour)       # 11
print(datem.minute)     # 22
print(datem.second)     # 3