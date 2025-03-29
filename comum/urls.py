from django.urls import path
from .views import denuncia_create_view, lista_denuncias, DenunciaDetailView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("denunciar/", denuncia_create_view, name="denuncia_create"),
    path('denuncias/', lista_denuncias, name='lista_denuncias'),
    path('denuncias/<int:pk>/', DenunciaDetailView.as_view(), name='denuncia-detalhe'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)