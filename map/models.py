from django.db import models

# Create your models here.
class HouseRent(models.Model):
    url = models.CharField(max_length=255, unique=True, default='')
    title = models.TextField()
    bedroom_count = models.IntegerField(null=True)
    livingroom_count = models.IntegerField(null=True)
    house_area = models.FloatField()
    house_name = models.TextField(null=True)
    updated_date = models.DateField()
    address = models.TextField(null=True, default='')
    district = models.TextField(null=True, default='')
    city = models.TextField(null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    price = models.FloatField()
    source = models.TextField()