from django import forms
from .models import Denuncia
from .enums import tipo_maus_tratos_choices


class DenunciaForm(forms.ModelForm):
    tipo_maustratos = forms.MultipleChoiceField(
        choices=tipo_maus_tratos_choices,
        widget=forms.CheckboxSelectMultiple,
        label="Tipo de Maus-Tratos"
    )

    class Meta:
        model = Denuncia
        exclude = ['data_denuncia']  # Exclui campo auto_now_add

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Se estiver editando, converte a string de volta para lista
        if self.instance.pk and self.instance.tipo_maustratos:
            self.initial['tipo_maustratos'] = self.instance.tipos_maustratos_list

    def clean_tipo_maustratos(self):
        """Valida e retorna a lista de valores (o model cuidará da conversão)"""
        tipos = self.cleaned_data.get('tipo_maustratos', [])

        # Verifica se os valores estão nas opções válidas
        valid_choices = [choice[0] for choice in tipo_maus_tratos_choices]
        for tipo in tipos:
            if tipo not in valid_choices:
                raise forms.ValidationError(f"'{tipo}' não é uma opção válida.")

        return tipos