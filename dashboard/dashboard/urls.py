from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static  # Import static here
from . import settings
from dashboardapp import views  # Import views from the app

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('dashboardapp.urls')),

    # Front page
    path('', views.index, name='front-page'),

    # Soils and Borehole Summary pages
    path('soils/', views.soils, name='soils'),
    path('boreholesummary/', views.boreholesummary, name='boreholesummary'),

    # File upload page
    path("upload/", views.upload_file, name="upload_file"),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
