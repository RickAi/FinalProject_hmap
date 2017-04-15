# Create your views here.
from django.http import JsonResponse
from map.models import *

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