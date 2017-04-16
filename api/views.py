# Create your views here.
from django.db.models import Avg, Max
from django.http import JsonResponse
from map.models import *
import ast

def boundaries(request):
    geojson = {'type': "FeatureCollection"}

    geo_list = []
    avg_list = []
    for geo_info in Geoinfo.objects.all():
        properties = ast.literal_eval(geo_info.properties)
        geometry = ast.literal_eval(geo_info.geometry)

        # query from database
        properties['avg_roi'] = RoiResult.objects.filter(district=geo_info.district).aggregate(Avg('roi')).get(
            'roi__avg')
        properties['max_roi'] = RoiResult.objects.filter(district=geo_info.district).aggregate(Max('roi')).get(
            'roi__max')

        if properties['avg_roi'] is not None:
            avg_list.append(properties['avg_roi'])

        feature = {'type': "Feature", 'properties': properties, 'geometry': geometry}
        geo_list.append(feature)

    geojson['features'] = geo_list
    return JsonResponse(geojson)

def points(request):
    roi_results = RoiResult.objects.all()

    points = list()
    for roi_result in roi_results:
        if roi_result.latitude == 0 or roi_result.longitude == 0:
            continue
        points.append([roi_result.latitude, roi_result.longitude, str(roi_result.id)])

    return JsonResponse(points, safe=False)

def point_detail(request):
    roi_id = request.GET.get('roi_id', '')
    if roi_id == '':
        return "<p>Query failed!</p>"

    roi = RoiResult.objects.get(id=roi_id)
    rent = HouseRent.objects.get(id=roi.rent_id)
    sale = HouseSale.objects.get(id=roi.sale_id)

    json_result = {'updated_date': roi.updated_date}
    if roi.is_from_rent == 1:
        json_result['title'] = rent.title
        json_result['bedroom_count'] = rent.bedroom_count
        json_result['livingroom_count'] = rent.livingroom_count
        json_result['house_area'] = rent.house_area
        json_result['house_name'] = rent.house_name
        json_result['rent_price'] = rent.price
        json_result['total_price'] = sale.total_price
        json_result['source'] = rent.source
    else:
        json_result['title'] = sale.title
        json_result['bedroom_count'] = sale.bedroom_count
        json_result['livingroom_count'] = sale.livingroom_count
        json_result['house_area'] = sale.house_area
        json_result['house_name'] = sale.house_name
        json_result['rent_price'] = rent.price
        json_result['total_price'] = sale.total_price
        json_result['source'] = sale.source

    return JsonResponse(json_result)