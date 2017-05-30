from map.models import *

# add more features into geoinfo db
def run():
    geoinfos = Geoinfo.objects.all()

    for geo in geoinfos:
        geo.house_count = RoiResult.objects.filter(district=geo.district).count()
        geo.save()