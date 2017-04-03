from django.shortcuts import render_to_response

from map.models import HouseRent


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
    rents = HouseRent.objects.all()
    datas = list()
    for rent in rents:
        if rent.latitude == 0 or rent.longitude == 0:
            continue
        datas.append([rent.latitude, rent.longitude])
    print("data count:" + str(len(datas)))
    return render_to_response('point_map.html', {'datas': datas})


def choropleth_map(request):
    return render_to_response('choropleth_map.html')
