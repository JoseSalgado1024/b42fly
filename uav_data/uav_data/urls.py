from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='B4uFly DPS')

urlpatterns = [
    path(r'api/v1/', include('api.urls')),
    path(r'api/docs', schema_view),
    path('admin/', admin.site.urls),
]
