import datetime
import random

from map.models import ProcessHistory

def run():
    for cur in range(0, 7):
        date = datetime.datetime.now() - datetime.timedelta(days=(7-cur))
        roi = random.uniform(1.8, 2.8)
        ProcessHistory.create(date.strftime("%Y-%m-%d"), roi).save()
