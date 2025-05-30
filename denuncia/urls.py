from django.contrib import admin
from django.urls import path, include
from comum.views import denuncia_create_view,lista_denuncias,painel_denuncias, denuncia_detail_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', denuncia_create_view, name='home'),
    path("denunciar/", include("comum.urls")),
    path('denuncias/', lista_denuncias, name='lista_denuncias'),
    path('denuncias/<int:pk>/', denuncia_detail_view, name='denuncia-detalhe'),
    path('painel_denuncias/', painel_denuncias, name='painel_denuncias'),
    path('adm/', include('adm.urls', namespace='adm')),
    path('formulario-denuncia/', denuncia_create_view, name='formulario_denuncia'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




