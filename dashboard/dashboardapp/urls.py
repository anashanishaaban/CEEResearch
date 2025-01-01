from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),  # URL for the index.html
    path('soils/', views.soils, name='soils'),
    path('boreholesummary/', views.boreholesummary, name='boreholesummary'),
    path("upload/", views.upload_file, name="upload_file"),
]