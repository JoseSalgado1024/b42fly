# from django.db import models
from django.contrib.gis.db import models


# Create your models here.
class Restriction(models.Model):
    """

    """


class ExtraField(models.Model):
    """
    Extra field
    """


class Zone(models.Model):
    """

    """
    name = models.CharField('Zone name', max_length=10, default='')
    description = models.CharField('Zone description', max_length=300, default='')
    polygon = models.MultiPolygonField('Zone polygon')

    def __str__(self):
        return '' % self.name
