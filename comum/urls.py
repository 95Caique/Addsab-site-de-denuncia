from django.urls import path
from .views import denuncia_create_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("denunciar/", denuncia_create_view, name="denuncia_create"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)