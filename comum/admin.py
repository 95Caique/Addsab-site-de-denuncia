from django.contrib import admin
from.models import Denuncia

@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ("especie", "local", "tipo_maustratos", "data_denuncia")
    search_fields = ("especie", "local", "responsavel")
    list_filter = ("tipo_maustratos", "data_denuncia")