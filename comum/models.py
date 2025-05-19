from django.db import models
from django.contrib.auth.models import User
from .enums import tipo_maus_tratos_choices, STATUS_DENUNCIA_CHOICES
from django.utils.safestring import mark_safe
from django.utils import timezone
import os

class Denuncia(models.Model):
    especie = models.CharField("Espécie do Animal", max_length=50)
    nome = models.CharField("Nome do Animal", max_length=50, blank=True, null=True)
    raca = models.CharField("Raça", max_length=50, blank=True, null=True)
    idade = models.CharField("Idade Aproximada", max_length=50, blank=True, null=True)
    descricao_animal = models.TextField("Descrição do Animal", blank=True, null=True)
    local = models.CharField ("Endereço do Caso", max_length=255, blank=True, null=True)
    tipo_maustratos = models.TextField("Tipo de Maus-Tratos")
    descricao_caso = models.TextField("Descrição detalhada dos Maus-Tratos")
    responsavel = models.CharField("Nome ou características do responsável pelo animal", max_length=50, blank=True, null=True)
    imagens = models.FileField("Anexe fotos ou vídeos", upload_to='comprovacoes/', blank=True, null=True)
    nome_denunciante = models.CharField ("Nome do Denunciante", max_length=100, blank=True, null=True,
    help_text="Sua identificação não é obrigatória, identifique-se apenas se quiser!" )
    email = models.EmailField("Email", blank=True, null=True)
    telefone = models.CharField("Telefone", max_length=50, blank=True, null=True)

    data_denuncia = models.DateTimeField("Data da Denúncia", auto_now_add=True)
    status = models.CharField("Status", max_length=20, choices=STATUS_DENUNCIA_CHOICES, default='recebida')
    
    atendente_responsavel = models.ForeignKey(
        User,
        verbose_name="Atendente Responsável",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='denuncias_atribuidas'
    )
    data_atribuicao = models.DateTimeField("Data de Atribuição", null=True, blank=True)
    ultima_atualizacao = models.DateTimeField("Última Atualização", auto_now=True)

    class Meta:
        verbose_name = "Denúncia"
        verbose_name_plural = "Denúncias"
        ordering = ['-data_denuncia']

    def __str__(self):
        return f"Denúncia: {self.especie} em {self.local or 'local não informado'}"

    def atribuir_atendente(self, atendente):
        """Atribui um atendente à denúncia"""
        self.atendente_responsavel = atendente
        self.data_atribuicao = timezone.now()
        self.status = 'processando'
        self.save()

    def remover_atendente(self):
        """Remove o atendente atribuído à denúncia"""
        self.atendente_responsavel = None
        self.data_atribuicao = None
        self.status = 'recebida'
        self.save()

    @property
    def tipos_maustratos_list(self):
        """Retorna a lista de tipos de maus-tratos."""
        if not self.tipo_maustratos:
            return []
        return self.tipo_maustratos.split(',')

    def get_tipos_formatados(self):
        """Retorna os tipos de maus-tratos formatados para exibição."""
        from .enums import tipo_maus_tratos_choices
        tipos_dict = dict(tipo_maus_tratos_choices)
        tipos_list = [tipo.strip() for tipo in self.tipo_maustratos.split(",") if tipo.strip()]
        return ", ".join([tipos_dict.get(tipo, tipo) for tipo in tipos_list])

    def save(self, *args, **kwargs):
        # Se tipo_maustratos for uma lista, converte para string
        if isinstance(self.tipo_maustratos, (list, tuple)):
            self.tipo_maustratos = ','.join(self.tipo_maustratos)
        super().save(*args, **kwargs)

class Tratativa(models.Model):
    denuncia = models.ForeignKey(
        Denuncia,
        on_delete=models.CASCADE,
        related_name='tratativas'
    )
    atendente = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    descricao = models.TextField("Descrição da Tratativa")
    data_tratativa = models.DateTimeField("Data da Tratativa", auto_now_add=True)
    status_anterior = models.CharField(max_length=20, choices=STATUS_DENUNCIA_CHOICES)
    status_novo = models.CharField(max_length=20, choices=STATUS_DENUNCIA_CHOICES)

    class Meta:
        ordering = ['-data_tratativa']
        verbose_name = "Tratativa"
        verbose_name_plural = "Tratativas"

    def __str__(self):
        return f"Tratativa da denúncia {self.denuncia.id} por {self.atendente.get_full_name() or self.atendente.username}"

class ComentarioDenuncia(models.Model):
    denuncia = models.ForeignKey('Denuncia', on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_criacao']

    def __str__(self):
        return f'Comentário de {self.autor.get_full_name()} em {self.data_criacao}'

class AnexoDenuncia(models.Model):
    denuncia = models.ForeignKey('Denuncia', on_delete=models.CASCADE, related_name='anexos')
    arquivo = models.FileField(upload_to='anexos_denuncia/')
    nome = models.CharField(max_length=255)
    anexado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data_anexo = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_anexo']

    def __str__(self):
        return self.nome

    @property
    def nome_arquivo(self):
        return os.path.basename(self.arquivo.name)
