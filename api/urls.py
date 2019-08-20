from django.urls import path

from . import views

urlpatterns = [
    path('upload_link', views.upload_link, name='upload_link'),
    path('upload/<slug:token>', views.ImageUploadView.as_view(), name='upload'),
    path('<int:id>', views.get_image, name='image'),
    path('statistics', views.statistics, name='statistics'),
]
