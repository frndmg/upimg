from django.urls import path

urlpatterns = [
    path('upload_link', views.upload_link, name='upload_link'),
    path('upload/<slug:token>', views.upload, name='upload'),
    path('<int:id>', views.get_image, name='image'),
    path('statistics', views.statistics, name='statistics'),
]
