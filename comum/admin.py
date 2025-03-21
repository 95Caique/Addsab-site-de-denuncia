from django.contrib import admin
from .models import Denuncia
from .enums import tipo_maus_tratos_choices


@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ("especie", "local", "get_tipos_formatados", "data_denuncia")
    search_fields = ("especie", "local", "responsavel", "tipo_maustratos")
    list_filter = ("data_denuncia", "especie")
    readonly_fields = ("data_denuncia",)

    def get_tipos_formatados(self, obj):
        """Formata os tipos de maus-tratos para exibição"""
        tipos_dict = dict(tipo_maus_tratos_choices)
        return ", ".join([tipos_dict.get(tipo, tipo) for tipo in obj.tipos_maustratos_list])

    get_tipos_formatados.short_description = "Tipos de Maus-Tratos"

    # Filtro personalizado para tipo_maustratos
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Permite buscar por termos contidos no tipo_maustratos
        if search_term:
            tipo_qs = Denuncia.objects.filter(tipo_maustratos__icontains=search_term)
            queryset = queryset | tipo_qs

        return queryset, use_distinct