# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('policy/', views.PolicyLCView.as_view(), name='policy-lc'),
    path('policy/<str:pk>/', views.PolicyRUDView.as_view(), name='policy-rud'),
    path('collection/', views.GeometryCollectionLCView.as_view(), name='collection-lc'),
    path('collection/<str:pk>/', views.GeometryCollectionRUDView.as_view(), name='collection-rud'),
    path('point/', views.PointFeatureLCView.as_view(),
         name='point-lc'),
    path('point/near/<lng>/<lat>/<buffer>/',
         views.SearchNearPoints.as_view(),
         name='point-search'),
    path('point/<str:pk>/', views.PointFeatureRUDView.as_view(), name='point-rud'),
    path('area/', views.AreaFeatureLCView.as_view(), name='area-lc'),
    path('area/near/<lng>/<lat>/<buffer>/',
         views.SearchNearPoints.as_view(), name='area-search'),
    path('area/<str:pk>/', views.PointFeatureRUDView.as_view(), name='area-rud'),
]
