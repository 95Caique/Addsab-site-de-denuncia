from django.db import models
from .enums import tipo_maus_tratos_choices

class Denuncia(models.Model):
    especie = models.CharField("Espécie do Animal", max_length=50)
    nome = models.CharField("Nome do Animal", max_length=50, blank=True, null=True)
    raca = models.CharField("Raça", max_length=50, blank=True, null=True)
    idade = models.CharField("Idade Aproximada", max_length=50, blank=True, null=True)
    Descricao_animal = models.TextField("Descrição do Animal")
    local = models.CharField ("Endereço do Caso", max_length=255, blank=True, null=True)
    tipo_maustratos = models.CharField("Tipo de Maus-Tratos", max_length=200, choices=tipo_maus_tratos_choices)
    descricao_caso = models.TextField("Descrição detalhada dos Maus-Tratos")
    responsavel = models.CharField("Nome do responsável pelo animal", max_length=50, blank=True, null=True)
    comprovacao = models.FileField("Anexe fotos ou vídeos", upload_to='comprovacoes/', blank=True, null=True)
    nome_denunciante = models.CharField ("Nome do Denunciante", max_length=100, blank=True, null=True,
    help_text="Sua identificação não é obrigatória, identifiqu-se apenas se quiser!" )
    email = models.EmailField("Email", blank=True, null=True)
    telefone = models.CharField("Telefone", max_length=50, blank=True, null=True)

    data_denuncia = models.DateTimeField("Data da Denúncia", auto_now_add=True)

    def __str__(self):
        return f"Denúncia - {self.especie} em {self.local}"


