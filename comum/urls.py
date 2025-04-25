from django.urls import path
from .views import denuncia_create_view, painel_denuncias, lista_denuncias, DenunciaDetailView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("denuncia/", denuncia_create_view, name="denuncia_create"),
    path('denuncias/', lista_denuncias, name='lista_denuncias'),
    path('denuncias/<int:pk>/', DenunciaDetailView.as_view(), name='denuncia-detalhe'),
    path('painel_denuncias/', painel_denuncias, name='painel_denuncias'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)