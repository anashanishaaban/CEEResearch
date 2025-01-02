from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),  # URL for the index.html
    path('soils/', views.soils, name='soils'),
    path('boreholesummary/', views.boreholesummary, name='boreholesummary'),
    path("upload/", views.upload_file, name="upload_file"),
    path('update-table', views.update_table, name='update_table'),  # No trailing slash here
    path('process-references', views.process_references, name='process_references'),  # No trailing slash here
]