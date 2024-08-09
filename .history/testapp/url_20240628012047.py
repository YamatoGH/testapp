from django.urls import path
from . import views
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', views.home, name='home'),
    path('test/<int:test_id>/', views.test_detail, name='test_detail'),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('testapp.urls')),
]
