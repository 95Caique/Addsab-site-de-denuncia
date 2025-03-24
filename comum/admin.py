from django.contrib import admin
from django.utils.html import format_html
from .models import Denuncia
from .enums import tipo_maus_tratos_choices


@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    # Campos visíveis no formulário de edição
    fields = ('especie', 'nome', 'raca', 'idade', 'descricao_animal', 'local', 'tipo_maustratos', 'descricao_caso',
              'responsavel', 'imagens', 'nome_denunciante', 'email', 'telefone', 'data_denuncia', )

    # Campos exibidos na listagem no Admin
    list_display = (
        'imagens',  # Miniatura da imagem ou link do vídeo
        'especie',
        'local',
        'nome_denunciante',
        'get_tipos_formatados',
        'data_denuncia',

    )

    # Campos clicáveis na listagem
    list_display_links = ['especie', 'local']

    # Filtros da listagem
    list_filter = ['data_denuncia', 'especie']

    # Campos apenas leitura no formulário de edição
    readonly_fields = ('data_denuncia', 'admin_photo')

    def get_tipos_formatados(self, obj):
        """Formata os tipos de maus-tratos para exibição"""
        tipos_dict = dict(tipo_maus_tratos_choices)
        tipos_list = [tipo.strip() for tipo in obj.tipo_maustratos.split(",") if tipo.strip()]
        return ", ".join([tipos_dict.get(tipo, tipo) for tipo in tipos_list])

    get_tipos_formatados.short_description = "Tipos de Maus-Tratos"

    def admin_photo(self, obj):
        """Exibe uma miniatura da imagem ou link para o vídeo no admin"""
        if obj.comprovacao:
            file_url = obj.comprovacao.url  # Obtém a URL completa do arquivo

            # Se for uma imagem, exibe a miniatura
            if file_url.lower().endswith(('webp', 'jpg', 'jpeg', 'png', 'gif')):
                return format_html('<img src="{}" width="100" />', file_url)

            # Se for um vídeo, exibe um link
            elif file_url.lower().endswith(('mp4', 'mov', 'avi', 'mkv')):
                return format_html('<a href="{}" target="_blank">Visualizar vídeo</a>', file_url)

        return "Nenhum arquivo"  # Caso não haja arquivo

    admin_photo.short_description = 'Comprovação (Foto/Vídeo)'  # Descrição do campo no admin
    admin_photo.allow_tags = True  # Permite a renderização de HTML no campo
