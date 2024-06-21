
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('noticias/', include('caosnoticias.urls')),
    path('sesion/', include('RegisterAndLogin.urls')),
]
