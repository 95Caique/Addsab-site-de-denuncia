from django.contrib import admin
from django.urls import path
from comum.views import denuncia_create_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('denuncia/', denuncia_create_view, name='denuncia'),
]





