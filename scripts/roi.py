from map.models import *
import time
import requests

BASE_URL = "http://apis.map.qq.com/ws/geocoder/v1/"
KEY_REVERSE_ADDRESS = [
    "OP4BZ-VBG3J-R3WF2-FQL4X-IFYCT-HBFFW",
    "L2TBZ-PZCKF-FFAJY-JMMTB-NTEUT-BJFSQ",
    "OKFBZ-ZXTCF-JKUJS-J3ZHS-AFCUT-VTBSQ",
    "L3DBZ-LVFWI-75VG2-5MMRI-5PWST-IEBJO",
    "BNZBZ-DILKU-UTMVN-4BL2P-LEX5H-BXBJW",
    "OTBBZ-BSJKP-VRADN-VO5BN-WDEKV-O7BVQ",
    "GWKBZ-JM2CS-AMFOP-6MWUF-GFXYF-LSBJA",
    "VA2BZ-QJTKW-QXPRL-OTH5N-7IKQ3-RTFJT",
    "KP4BZ-K4WCJ-63SFM-FOPG4-WOKCF-XSBFS",
    "RFTBZ-FQACP-EPADZ-L44KV-KVAO2-FLFDM",
]
PARAMETER_LOCATION = "location"
PARAMETER_KEY = "key"
TABLE_NAME_RENT = "map_houserent"
TABLE_NAME_SALE = "map_housesale"

current_key_index = 0

# calculate roi, contain a series operations here
# 1. Closest geo point calculated with mysql
# 2. Reverse location from latitude and longitude
# 3. 10 keys

def run():
    crontab_roi()

def crontab_roi():
    last_process = ProcessHistory.objects.latest().process_date
    current_date = time.strftime("%Y-%m-%d")

    try:
        process_from_rents(last_process, current_date)
        print("process_from_rents DONE!")
        process_from_sales(last_process, current_date)
        print("process_from_sales DONE!")
    except:
        print("Break!")
    finally:
        ProcessHistory.create(current_date).save()
        print("process DONE!")

def update_geo_info():
    pass

def process_from_rents(last_process, current_date):
    new_rents = HouseRent.objects.filter(updated_date__gte=last_process)

    for rent in new_rents:
        if rent.latitude == 0 or rent.longitude == 0:
            print("Invalid location!")
            continue

        query_string = "SELECT id, (6371 * acos(cos(radians(%s)) * cos(radians(latitude)) * cos(radians(longitude)" \
                       " - radians(%s)) + sin(radians(%s)) * sin(radians(latitude)))) AS distance FROM" \
                       " %s HAVING distance < 5 ORDER BY distance;" % (
                           rent.latitude, rent.longitude, rent.latitude, TABLE_NAME_SALE)

        query_result = HouseSale.objects.raw(query_string)
        if len(list(query_result)) == 0:
            print("No matched location!")
            continue
        closest_sale = query_result[0]

        try:
            RoiResult.objects.get(rent_id=rent.id, sale_id=closest_sale.id)
            print("Already exist!")
            continue
        except:
            pass

        roi = ((rent.price * 12) / (closest_sale.total_price * 10000)) * 100
        district = query_district(rent.latitude, rent.longitude)

        try:
            RoiResult.create(district, True, rent.id, closest_sale.id, current_date, roi, rent.latitude,
                             rent.longitude).save()
            print("Generate new one from rent!")
        except:
            print("Insert error!")


def process_from_sales(last_process, current_date):
    new_sales = HouseSale.objects.filter(updated_date__gte=last_process)

    for sale in new_sales:
        if sale.latitude == 0 or sale.longitude == 0:
            print("Invalid location!")
            continue

        query_string = "SELECT id, (6371 * acos(cos(radians(%s)) * cos(radians(latitude)) * cos(radians(longitude)" \
                       " - radians(%s)) + sin(radians(%s)) * sin(radians(latitude)))) AS distance FROM" \
                       " %s HAVING distance < 5 ORDER BY distance;" % (
                           sale.latitude, sale.longitude, sale.latitude, TABLE_NAME_RENT)

        # search closest
        query_result = HouseRent.objects.raw(query_string)
        if len(list(query_result)) == 0:
            print("No matched location!")
            continue
        closest_rent = query_result[0]

        # duplicate match
        try:
            RoiResult.objects.get(rent_id=closest_rent.id, sale_id=sale.id)
            print("Already exist!")
            continue
        except:
            pass

        # calculate roi
        roi = ((closest_rent.price * 12) / (sale.total_price * 10000)) * 100
        district = query_district(closest_rent.latitude, closest_rent.longitude)

        # create
        try:
            RoiResult.create(district, False, closest_rent.id, sale.id, current_date, roi, closest_rent.latitude,
                             closest_rent.longitude).save()
            print("Generate new one from sale!")
        except:
            print("Insert error!")


def query_district(latitude, longitude):
    global current_key_index

    api_url = (BASE_URL + "?" + PARAMETER_LOCATION + "=%s,%s" + "&" + PARAMETER_KEY + "=" + KEY_REVERSE_ADDRESS[
        current_key_index]) % (
                  latitude, longitude)
    result = ''
    json_result = ''
    while result == '':
        try:
            result = requests.get(api_url)
            json_result = result.json()
        except:
            print("Connection refused by the server!")
            time.sleep(5)

    if json_result.get('status') == 0:
        return json_result.get('result').get('address_component').get('district')
    else:
        current_key_index += 1
        print("Change key!")
        return query_district(latitude, longitude)