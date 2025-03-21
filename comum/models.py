from django.db import models
from .enums import tipo_maus_tratos_choices

class Denuncia(models.Model):
    especie = models.CharField("Espécie do Animal", max_length=50)
    nome = models.CharField("Nome do Animal", max_length=50, blank=True, null=True)
    raca = models.CharField("Raça", max_length=50, blank=True, null=True)
    idade = models.CharField("Idade Aproximada", max_length=50, blank=True, null=True)
    descricao_animal = models.TextField("Descrição do Animal", blank=True, null=True)
    local = models.CharField ("Endereço do Caso", max_length=255, blank=True, null=True)
    tipo_maustratos = models.TextField("Tipo de Maus-Tratos")
    descricao_caso = models.TextField("Descrição detalhada dos Maus-Tratos")
    responsavel = models.CharField("Nome do responsável pelo animal", max_length=50, blank=True, null=True)
    comprovacao = models.FileField("Anexe fotos ou vídeos", upload_to='comprovacoes/', blank=True, null=True)
    nome_denunciante = models.CharField ("Nome do Denunciante", max_length=100, blank=True, null=True,
    help_text="Sua identificação não é obrigatória, identifiqu-se apenas se quiser!" )
    email = models.EmailField("Email", blank=True, null=True)
    telefone = models.CharField("Telefone", max_length=50, blank=True, null=True)

    data_denuncia = models.DateTimeField("Data da Denúncia", auto_now_add=True)

    class Meta:
        verbose_name = "Denúncia"
        verbose_name_plural = "Denúncias"
        ordering = ['-data_denuncia']

    def __str__(self):
        return f"Denúncia: {self.especie} em {self.local or 'local não informado'}"

    @property
    def tipos_maustratos_list(self):
        """Retorna a lista de tipos de maus-tratos."""
        if not self.tipo_maustratos:
            return []
        return self.tipo_maustratos.split(',')

    def save(self, *args, **kwargs):
        # Se tipo_maustratos for uma lista, converte para string
        if isinstance(self.tipo_maustratos, (list, tuple)):
            self.tipo_maustratos = ','.join(self.tipo_maustratos)
        super().save(*args, **kwargs)
