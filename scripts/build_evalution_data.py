import operator

from map.models import *

TABLE_NAME_RENT = "map_houserent"
TABLE_NAME_SALE = "map_housesale"

class Temp:
    def __init__(self, latitude, longitude, rent_price, total_price):
        self.latitude = latitude
        self.longitude = longitude
        self.rent_price = rent_price
        self.total_price = total_price

def run():
    rents = HouseRent.objects.all()

    data = {}
    num = 0
    for rent in rents:
        if rent.latitude == 0 or rent.longitude == 0:
            continue
        query_string = "SELECT id, (6371 * acos(cos(radians(%s)) * cos(radians(latitude)) * cos(radians(longitude)" \
                           " - radians(%s)) + sin(radians(%s)) * sin(radians(latitude)))) AS distance FROM" \
                           " %s HAVING distance < 0.001 ORDER BY distance;" % (
                               rent.latitude, rent.longitude, rent.latitude, TABLE_NAME_SALE)
        query_result = HouseSale.objects.raw(query_string)
        count = len(list(query_result))
        if count > 0:
            evaluate = EvaluateData.objects.filter(latitude=rent.latitude, longitude=rent.longitude)
            if len(list(evaluate)) != 0:
                continue
            num += 1
            if num > 100:
                break
            EvaluateData.create(rent.latitude, rent.longitude, rent.price, query_result[0].per_price * rent.house_area, rent.house_area).save()
            # temp = Temp(rent.latitude, rent.longitude, rent.price, query_result[0].total_price)
            # data[temp] = count
            print(count)

    # get top 100
    # data_tuple = sorted(data.items(), key=operator.itemgetter(1), reverse=True)
    # for cur in range(0, 100):
    #     cur_data = data_tuple[cur]
    #     cur_temp = cur_data[0]
    #     EvaluateData.create(cur_temp.latitude, cur_temp.longitude, cur_temp.rent_price, cur_temp.total_price).save()