from django.contrib import admin
from django.urls import path, include
from comum.views import denuncia_create_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', denuncia_create_view, name='home'),
    path("denunciar/", include("comum.urls")),
]





