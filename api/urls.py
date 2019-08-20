from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

urlpatterns = [
    path('upload_link', views.upload_link, name='upload_link'),
    path('upload/<slug:token>', views.upload_image, name='upload'),
    path('<int:pk>', views.get_image, name='get_image'),
    path('statistics', views.statistics, name='statistics'),
] + router.urls
