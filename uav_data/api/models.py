# from django.db import models
from django.contrib.gis.db import models

# Create your models here.

POLICY_TYPES_CHOICES = (
    ('forbidden', 'Forbidden'),
    ('warning', 'Warning'),
    ('allowed', 'Allowed'),
)


class Policy(models.Model):
    """

    """

    identifier = models.CharField(default='', primary_key=True, max_length=32)
    name = models.CharField(max_length=50, default='')
    description = models.TextField(blank=True)
    top_altitude = models.FloatField(default=0.0)
    max_operator_distance = models.FloatField(default=0.0)
    max_uav_weight = models.FloatField(default=0.0)
    start_at = models.DateField(auto_now=True, blank=True)
    expiration_time = models.DateField(null=True, blank=True)
    don_t_expire = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % self.identifier

    class Meta:
        ordering = ('name', )


class GeometryCollection(models.Model):
    """

    """
    class Meta:
        ordering = ('name', )

    identifier = models.CharField(unique=True, max_length=32, default='', primary_key=True)
    name = models.CharField('Zone name', max_length=40, default='')
    description = models.CharField('Zone description', max_length=300, default='')

    def __str__(self):
        return '%s' % self.identifier


class GeometryCollectionAbstract(models.Model):
    """

    """
    class Meta:
        abstract = True

    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, default='')
    geometry_collection = models.ForeignKey(GeometryCollection, on_delete=models.CASCADE, default='')


class PointFeature(GeometryCollectionAbstract):
    """

    """
    # Geographical point
    point = models.PointField('Point Field')
    identifier = models.CharField(max_length=40, unique=True, primary_key=True, default='')
    name = models.CharField(max_length=40, default='')
    description = models.TextField(default='', null=True, blank='')

    def __str__(self):
        return '%s:%s' % (self.identifier, self.name)


class AreaFeature(GeometryCollectionAbstract):
    """

    """
    # Geographical Polygon
    polygon = models.PolygonField('Polygon Field')
    identifier = models.CharField(max_length=40, unique=True, primary_key=True, default='')
    name = models.CharField(max_length=40, default='')
    description = models.TextField(default='', null=True, blank='')

    def __str__(self):
        return '%s:%s' % (self.identifier, self.name)


class ExtraField(GeometryCollectionAbstract):
    """
    Extra field
    """
    key = models.CharField('Key, Value identifier', max_length=20, default='')
    value = models.CharField(max_length=500, default='')

    class Meta:
        ordering = ('key', )

    def __str__(self):
        return '%s:%s' % (self.key, self.value)
