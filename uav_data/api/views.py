from .serializers import *
from .models import *
from rest_framework import generics
from rest_framework.views import *
from rest_framework.exceptions import *
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json


@login_required
def dashboard(request):
    user = request.user
    auth0user = user.social_auth.get(provider="auth0")
    userdata = {'user_id': auth0user.uid, 'name': user.first_name, 'picture': auth0user.extra_data['picture']}
    return render(request, 'dashboard.html', {'auth0User': auth0user, 'userdata': json.dumps(userdata, indent=4)})


def index(request):
    return render(request, 'home.html')


class GeometryCollectionLCView(generics.ListCreateAPIView):
    queryset = GeometryCollection.objects.all()
    serializer_class = GeometryCollectionListSerializer


class GeometryCollectionRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GeometryCollection.objects.all()
    serializer_class = GeometryCollectionSerializer


class PolicyLCView(generics.ListCreateAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicyListSerializer


class PolicyRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer


class PointFeatureLCView(generics.ListCreateAPIView):
    queryset = PointFeature.objects.all()
    serializer_class = PointFeatureLCSerializer


class PointFeatureRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PointFeature.objects.all()
    serializer_class = PointFeatureSerializer


class AreaFeatureLCView(generics.ListCreateAPIView):
    queryset = AreaFeature.objects.all()
    serializer_class = AreaFeatureSerializerLC


class AreaFeatureRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AreaFeature.objects.all()
    serializer_class = AreaFeatureSerializerRUD


class ExtraFieldsLCView(generics.ListCreateAPIView):
    queryset = ExtraField.objects.all()
    serializer_class = ExtraFieldSerializer


class ExtraFieldsRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExtraField.objects.all()
    serializer_class = ExtraFieldSerializer


class SearchNearObjects(APIView):
    model = None
    serializer = None

    def near_objects(self, poly, buffer, object_type='point'):
        if object_type not in ['point', 'polygon']:
            raise ValueError('objects_type: must be a str\'s instance and object_type in %s' % ['point', 'polygon'])
        q = {'%s__distance_lte' % object_type: (poly, D(m=buffer))}
        qs = self.model.objects.filter(**q)
        return self.serializer(qs, many=True).data


class SearchNearPoints(SearchNearObjects):
    """

    """
    model = PointFeature
    serializer = PointFeatureLCSerializer

    def get(self, request, lng=None, lat=None, buffer=None, _srid=4326):
        try:
            try:
                buffer = int(buffer)
                lng = float(lng)
                lat = float(lat)
            except ValueError:
                raise ValueError('Lat: must be an Float instance. Lng: must be an Float instance. '
                                 'Buffer: must be an integer instance.')
            if not -90.0 <= lat <= 90.0:
                raise ValueError('Lat: must be less or equal than 90.0 and greater or equal than -90.0')
            if not -180.0 <= lng <= 180.0:
                raise ValueError('Lng: must be less or equal than 180.0 and greater or equal than -180.0')
        except Exception as e:
            return Response({
                'msg': str(e),
                'status': status.HTTP_400_BAD_REQUEST,
            }, status=status.HTTP_400_BAD_REQUEST)
        np = self.near_objects(poly=Point(lng, lat, srid=_srid), buffer=buffer)
        return Response(np, status=status.HTTP_200_OK)
