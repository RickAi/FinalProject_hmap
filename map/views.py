import ast

from django.db.models import Avg
from django.db.models import Max
from django.shortcuts import render_to_response
from map.models import *

import json


def index(request):
    return


def cluster_map(request):
    rents = HouseRent.objects.all()
    datas = list()
    for rent in rents:
        if rent.latitude == 0 or rent.longitude == 0:
            continue
        datas.append([rent.latitude, rent.longitude, str(rent.price) + "/" + rent.source])
    print("data count:" + str(len(datas)))
    return render_to_response('cluster_map.html', {'datas': datas})


def heat_map(request):
    rents = HouseRent.objects.all()
    datas = list()
    for rent in rents:
        if rent.latitude == 0 or rent.longitude == 0:
            continue
        datas.append([rent.latitude, rent.longitude, rent.price / 8000])
    print("data count:" + str(len(datas)))
    return render_to_response('heat_map.html', {'datas': datas})


def point_map(request):
    rents = HouseSale.objects.all()
    datas = list()
    for rent in rents:
        if rent.latitude == 0 or rent.longitude == 0:
            continue
        datas.append([rent.latitude, rent.longitude])
    print("data count:" + str(len(datas)))
    return render_to_response('point_map.html', {'datas': datas})


def choropleth_map(request):
    geojson, max_avg = build_geojson()
    stages = build_stages(max_avg)
    rois = query_rois()
    return render_to_response('choropleth_map.html', {'geojson': geojson, 'stages': stages, 'rois': rois})


def build_geojson():
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
        # properties['min_roi'] = RoiResult.objects.filter(district=geo_info.district).aggregate(Min('roi')).get('roi__min')

        if properties['avg_roi'] is not None:
            avg_list.append(properties['avg_roi'])

        feature = {'type': "Feature", 'properties': properties, 'geometry': geometry}
        geo_list.append(feature)

    geojson['features'] = geo_list
    return json.dumps(geojson), max(avg_list)


def build_stages(max_avg):
    interval = max_avg / 8.0
    stages = []

    for cur in range(0, 8):
        stages.append("%.3f" % round(0 + cur * interval, 2))

    return stages

def query_rois():
    roi_results = RoiResult.objects.all()

    points = list()
    for roi_result in roi_results:
        if roi_result.latitude == 0 or roi_result.longitude == 0:
            continue
        points.append([roi_result.latitude, roi_result.longitude, str(roi_result.id)])

    return points