from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('basic.urls')),
    path('auth/', include('anmeldung_auth.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
]
