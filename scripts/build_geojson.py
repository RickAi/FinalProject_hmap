from map.models import Geoinfo
import json

def run():
    print(build_geojson())

def build_geojson():
    geojson = {'type': "FeatureCollection"}

    geo_list = []
    for geo_info in Geoinfo.objects.all():
        district = geo_info.district
        properties = geo_info.properties

        # query from database

        feature = {'type': "Feature", 'properties': properties, 'geometry': geo_info.geometry}
        geo_list.append(feature)

    geojson['features'] = geo_list
    return json.dumps(geojson)