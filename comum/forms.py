from django import forms
from .models import Denuncia
from .enums import tipo_maus_tratos_choices


class DenunciaForm(forms.ModelForm):
    tipo_maustratos = forms.MultipleChoiceField(
        choices=tipo_maus_tratos_choices,
        widget=forms.CheckboxSelectMultiple,
        label="Tipo de Maus-Tratos",
        required=True
    )

    class Meta:
        model = Denuncia
        exclude = ['data_denuncia']
        fields = ['especie', 'nome', 'raca', 'idade', 'descricao_animal', 'local', 
                 'tipo_maustratos', 'descricao_caso', 'responsavel', 'imagens', 
                 'nome_denunciante', 'email', 'telefone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Se estiver editando, converte a string de volta para lista
        if self.instance.pk and self.instance.tipo_maustratos:
            self.initial['tipo_maustratos'] = self.instance.tipo_maustratos.split(",")

    def clean_tipo_maustratos(self):
        """Converte a lista para string antes de salvar no banco"""
        tipos = self.cleaned_data.get('tipo_maustratos', [])

        # Valida se os valores são permitidos
        valid_choices = [choice[0] for choice in tipo_maus_tratos_choices]
        for tipo in tipos:
            if tipo not in valid_choices:
                raise forms.ValidationError(f"'{tipo}' não é uma opção válida.")

        return ",".join(tipos)

