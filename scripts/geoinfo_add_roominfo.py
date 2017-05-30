from map.models import *

def run():
    geoinfos = Geoinfo.objects.all()

    for geoinfo in geoinfos:
        # get all the rois in the district
        rois = RoiResult.objects.filter(district=geoinfo.district)

        one_room = 0
        two_room = 0
        three_room = 0
        more_room = 0
        for roi in rois:
            bc = 0
            if roi.is_from_rent == 1:
                bc = HouseRent.objects.filter(id=roi.rent_id)[0].bedroom_count
            else:
                bc = HouseSale.objects.filter(id=roi.sale_id)[0].bedroom_count

            if bc == 1:
                one_room += 1
            elif bc == 2:
                two_room += 1
            elif bc == 3:
                three_room += 1
            elif bc >= 4:
                more_room += 1

        json = {'1 Room': one_room, '2 Rooms': two_room, '3 Rooms': three_room, '4+ Rooms': more_room}
        geoinfo.room_info = json
        geoinfo.save()