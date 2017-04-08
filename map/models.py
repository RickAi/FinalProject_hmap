from django.db import models


# Create your models here.
class HouseRent(models.Model):
    url = models.CharField(unique=True, max_length=255)
    title = models.TextField(blank=True, null=True)
    bedroom_count = models.IntegerField(blank=True, null=True)
    livingroom_count = models.IntegerField(blank=True, null=True)
    house_area = models.FloatField(blank=True, null=True)
    house_name = models.TextField(blank=True, null=True)
    updated_date = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    district = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)

    class Meta:
        get_latest_by = "updated_date"


class HouseSale(models.Model):
    url = models.CharField(unique=True, max_length=255)
    title = models.TextField(blank=True, null=True)
    bedroom_count = models.IntegerField(blank=True, null=True)
    livingroom_count = models.IntegerField(blank=True, null=True)
    kitchen_count = models.IntegerField(blank=True, null=True)
    wc_count = models.IntegerField(blank=True, null=True)
    house_area = models.FloatField(blank=True, null=True)
    house_name = models.TextField(blank=True, null=True)
    updated_date = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    district = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    per_price = models.FloatField(blank=True, null=True)
    total_price = models.FloatField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)

    class Meta:
        get_latest_by = "updated_date"


class RoiResult(models.Model):
    district = models.TextField(blank=True, null=True)
    is_from_rent = models.IntegerField(blank=True, null=True)
    rent_id = models.IntegerField(blank=True, null=True)
    sale_id = models.IntegerField(blank=True, null=True)
    updated_date = models.DateField(blank=True, null=True)
    roi = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    @classmethod
    def create(cls, district, is_from_rent, rent_id, sale_id, updated_date, roi, latitude, longitude):
        return cls(district=district, is_from_rent=is_from_rent, rent_id=rent_id, sale_id=sale_id,
                   updated_date=updated_date, roi=roi, latitude=latitude, longitude=longitude)

    class Meta:
        get_latest_by = "updated_date"
        unique_together = (('rent_id', 'sale_id'),)


class ProcessHistory(models.Model):
    process_date = models.DateField(blank=True, null=True)

    @classmethod
    def create(cls, process_date):
        return cls(process_date=process_date)

    class Meta:
        get_latest_by = "process_date"


class Geoinfo(models.Model):
    id = models.IntegerField(primary_key=True)
    district = models.TextField()
    properties = models.TextField()
    geometry = models.TextField()

    @classmethod
    def create(cls, id, district, properties, geometry):
        return cls(id=id, district=district, properties=properties, geometry=geometry)
