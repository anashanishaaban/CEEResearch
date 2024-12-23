from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # URL for the index.html
    path('upload/', views.PointCloudUploadView.as_view(), name='pointcloud-upload'),
]