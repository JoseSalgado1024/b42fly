from rest_framework.serializers import *
from .models import *


class PolicySerializer(ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__'


class PolicyListSerializer(PolicySerializer):
    def to_representation(self, instance):
        return \
            {
                'identifier': instance.identifier,
                'name': instance.name,
                'web_url': '/api/v1/policy/%s' % instance.identifier,
            }


class GeometryCollectionSerializer(ModelSerializer):
    class Meta:
        model = GeometryCollection
        fields = '__all__'

    def to_representation(self, instance):
        points = PointFeatureLCSerializer(PointFeature.objects.filter(geometry_collection=instance.identifier),
                                          many=True)
        areas = AreaFeatureSerializerLC(AreaFeature.objects.filter(geometry_collection=instance.identifier), many=True)
        response = ModelSerializer.to_representation(self, instance)
        response.update({
            'points': points.data,
            'areas': areas.data
        })
        return response


class GeometryCollectionListSerializer(GeometryCollectionSerializer):
    def to_representation(self, instance):
        return \
            {
                'identifier': instance.identifier,
                'name': instance.name,
                'web_url': '/api/v1/collection/%s' % instance.identifier
            }


class PointFeatureSerializer(ModelSerializer):
    class Meta:
        model = PointFeature
        fields = '__all__'

    def to_representation(self, instance):
        response = ModelSerializer.to_representation(self, instance)
        response.update({'policy': PolicyListSerializer(instance.policy).data,
                         'geometry_collection': GeometryCollectionListSerializer(instance.geometry_collection).data})
        return response


class PointFeatureLCSerializer(PointFeatureSerializer):
    def to_representation(self, instance):
        return \
            {
                'identifier': instance.identifier,
                'name': instance.name,
                'web_url': '/api/v1/point/%s' % instance.identifier,
            }


class AreaFeatureSerializerRUD(ModelSerializer):
    class Meta:
        model = AreaFeature
        fields = '__all__'


class AreaFeatureSerializerLC(AreaFeatureSerializerRUD):
    def to_representation(self, instance):
        return \
            {
                'identifier': instance.identifier,
                'name': instance.name,
                'web_url': '/api/v1/area/%s' % instance.identifier,
            }
