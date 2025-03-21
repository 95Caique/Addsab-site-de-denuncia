from django.urls import path
from .views import denuncia_create_view

urlpatterns = [
    path("denunciar/", denuncia_create_view, name="denuncia_create"),

]
