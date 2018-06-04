from django.test import TestCase
from .views import *
from django.urls import reverse
from rest_framework import status
from django.contrib.gis.geos import Point, Polygon, LinearRing
from .utils import kwargs_match
import json
import os


HERE = os.path.dirname(os.path.abspath(__file__))


# Utils Test
class UtilsMatchKWArgs(TestCase):
    def test_string_representation(self):
        _default = {
            'key': '',
            'key2': '',
            'key3': '',
        }
        _amend = {'key': '1', 'key2': '2', 'key3': '3', }

        d = kwargs_match(_default, _amend)
        self.assertEqual(sorted(d), sorted(_amend))


# Views Tests
class PolicyTestCase(TestCase):

    test_data = json.loads(open(os.path.join(HERE, 'test.data/models.test.policy.json'), 'r').read())

    def test_01_get_policy_list(self):
        """
        Get policy list
        """
        response = self.client.get(reverse('policy-lc'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_02_get_policy_details(self):
        """
        Get Policy details
        """
        policy = Policy(**self.test_data)
        policy.save()
        response = self.client.get('/api/v1/policy/%s/' % policy.pk, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_03_policy_details_not_exists(self):
        """
        Not exists policy details
        """
        response = self.client.get('/api/v1/policy/%s/' % 'not-exists', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_04_policy_create(self):
        """
        Policy create
        """
        response = self.client.post(reverse('policy-lc'), {'identifier': 'uuid-other-policy',
                                                           'name': 'other-policy',
                                                           'start_at': '2018-06-02 04:20:00'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_05_serialize_all_fields(self):
        """

        """
        my_policy = Policy(**self.test_data)
        my_policy_serializer = PolicySerializer(my_policy)
        self.assertEqual(sorted(my_policy_serializer.data), sorted(self.test_data))

    def test_06_serialize_list_fields(self):
        """

        """
        my_policy = Policy(**self.test_data)
        my_policy_serializer = PolicyListSerializer(my_policy)
        self.assertEqual(sorted(my_policy_serializer.data),
                         sorted({"identifier": my_policy.identifier,
                                 "name": my_policy.name,
                                 'web_url': '/api/v1/policy/%s/' % my_policy.identifier}))

    def test_07_string_representation(self):
        """

        """
        my_new_policy = Policy(**self.test_data)
        self.assertEqual(str(my_new_policy), my_new_policy.identifier)


class GeometryCollectionTestCase(TestCase):

    test_data = json.loads(open(os.path.join(HERE, 'test.data/models.test.geometry-collection.json'), 'r').read())

    def test_01_get_geometry_collection_list(self):
        """
        Get geometry collection list
        """
        response = self.client.get(reverse('collection-lc'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_02_get_geometry_collection_details(self):
        """
        Get geometry collection details
        """
        geometry_collection = GeometryCollection(**self.test_data)
        geometry_collection.save()
        response = self.client.get('/api/v1/collection/%s/' % geometry_collection.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_03_geometry_collection_details_not_exists(self):
        response = self.client.get('/api/v1/collection/%s/' % 'not-exists')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_04_geometry_collection_create(self):
        """
        Geometry collection create
        """
        response = self.client.post('/api/v1/collection/', self.test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_01_serialize_all_fields(self):
        """

        """
        my_gc = GeometryCollection(**self.test_data)
        my_geometry_collection_serializer = GeometryCollectionSerializer(my_gc)
        test_data = self.test_data.copy()
        test_data.update({
            'points': [],
            'areas': [],
        })
        self.assertEqual(sorted(my_geometry_collection_serializer.data), sorted(test_data))

    def test_02_serialize_list_fields(self):
        """

        """
        my_gc = Policy(**self.test_data)
        my_policy_serializer = GeometryCollectionListSerializer(my_gc)
        self.assertEqual(sorted(my_policy_serializer.data),
                         sorted({"identifier": my_gc.identifier, "name": my_gc.name,
                                 'web_url': '/api/v1/collections/%s/' % my_gc.identifier}))

    def test_07_string_representation(self):
        """

        """
        my_new_gc = GeometryCollection(**self.test_data)
        self.assertEqual(str(my_new_gc), my_new_gc.identifier)


class ExtraFieldModelTest(TestCase):
    test_data = json.loads(open(os.path.join(HERE, 'test.data/models.test.extra-field.json'), 'r').read())

    def test_01_string_representation(self):
        """

        """
        my_new_ef = ExtraField(**self.test_data)
        self.assertEqual(str(my_new_ef), '%s:%s' % (my_new_ef.key, my_new_ef.value))


class PointAreaFeatureModelTest(TestCase):
    test_data = \
        {
            'geometry_collection': json.loads(
                open(os.path.join(HERE, 'test.data/models.test.geometry-collection.json'), 'r').read()),
            'policy': json.loads(open(os.path.join(HERE, 'test.data/models.test.policy.json'), 'r').read())
        }

    def test_01_point_feature_string_representation(self):
        """

        """
        test_data = self.test_data.copy()
        _point_data = json.loads(open(os.path.join(HERE, 'test.data/models.test.point-feature.json'), 'r').read())
        _point_data.update(dict(point=Point(_point_data.get('point'))))
        test_data.update(
            dict(
                policy=Policy(**self.test_data['policy']),
                geometry_collection=GeometryCollection(**self.test_data['geometry_collection']),
                **_point_data,
            ))
        my_new_pf = PointFeature(**test_data)
        self.assertEqual(str(my_new_pf), '%s:%s' % (my_new_pf.identifier, my_new_pf.name))

    def test_02_area_feature_string_representation(self):
        """

        """
        test_data = self.test_data.copy()
        _area_data = json.loads(open(os.path.join(HERE, 'test.data/models.test.area-feature.json'), 'r').read())
        _area_data.update(dict(polygon=Polygon(_area_data.get('polygon'))))
        test_data.update(
            dict(
                policy=Policy(**self.test_data['policy']),
                geometry_collection=GeometryCollection(**self.test_data['geometry_collection']),
                **_area_data,
            ))
        my_new_pf = AreaFeature(**test_data)
        self.assertEqual(str(my_new_pf), '%s:%s' % (my_new_pf.identifier, my_new_pf.name))

    def test_03_point_feature_list_view(self):
        """

        """
        response = self.client.get(reverse('point-lc'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_04_point_feature_details_view(self):
        """

        """
        test_data = self.test_data.copy()
        _point_data = json.loads(open(os.path.join(HERE, 'test.data/models.test.point-feature.json'), 'r').read())
        _point_data.update(dict(point=Point(_point_data.get('point'))))
        _geometry_collection = GeometryCollection(**test_data['geometry_collection'])
        _geometry_collection.save()
        _policy = Policy(**test_data['policy'])
        _policy.save()
        test_data.update(dict(policy=_policy,
                              geometry_collection=_geometry_collection,
                              **_point_data, ))
        point = PointFeature(**test_data)
        point.save()
        response = self.client.get('/api/v1/point/%s/' % point.identifier)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_05_point_feature_add_view(self):
        """

        """
        test_data = self.test_data.copy()
        data = json.loads(open(os.path.join(HERE, 'test.data/models.test.point-feature.json'), 'r').read())
        _geometry_collection = GeometryCollection(**test_data['geometry_collection'])
        _geometry_collection.save()
        _policy = Policy(**test_data['policy'])
        _policy.save()
        new_point = {
            'policy': _policy,
            'geometry_collection': _geometry_collection,
            'identifier': 'uuid-new-point',
            'name': 'new-point',
            'description': 'New point entry.',
            'point': Point(data.get('point'), srid=4326).json
        }
        response = self.client.post('/api/v1/point/', new_point)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_06_polygon_feature_list_view(self):
        response = self.client.get(reverse('area-lc'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_07_polygon_feature_details_view(self):
        """

        """
        test_data = self.test_data.copy()
        data = json.loads(open(os.path.join(HERE, 'test.data/models.test.area-feature.json'), 'r').read())
        geometry_collection = GeometryCollection(**test_data['geometry_collection'])
        geometry_collection.save()
        policy = Policy(**test_data['policy'])
        policy.save()
        test_data.update({
            'identifier': 'uuid-test-polygon',
            'name': 'test-polygon-details',
            'geometry_collection': geometry_collection,
            'description': 'new area description',
            'policy': policy,
            'polygon': Polygon(data.get('polygon'), srid=4326),
        })
        _polygon = AreaFeature(**test_data)
        _polygon.save()
        endpoint = '/api/v1/area/%s/' % _polygon.identifier
        response = self.client.get(endpoint)
        print(response)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_08_polygon_feature_add_view(self):
        """

        """
        test_data = self.test_data.copy()
        data = json.loads(open(os.path.join(HERE, 'test.data/models.test.area-feature.json'), 'r').read())
        geometry_collection = GeometryCollection(**test_data['geometry_collection'])
        geometry_collection.save()
        policy = Policy(**test_data['policy'])
        policy.save()
        data.update(
            {
                'identifier': 'uuid-test-post-polygon',
                'name': 'test-polygon',
                'geometry_collection': geometry_collection,
                'description': 'new area description',
                'policy': policy,
                'polygon': Polygon(data.get('polygon'), srid=4326).json
             })
        response = self.client.post(reverse('area-lc'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
