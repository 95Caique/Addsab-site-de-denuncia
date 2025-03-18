from django import forms
from .models import Denuncia

class DenunciaForm(forms.ModelForm):
    class Meta:
        model = Denuncia
        fields = '__all__'  # Inclui todos os campos do modelo
        widgets = {
            'tipo_maustratos': forms.CheckboxSelectMultiple(),
        }