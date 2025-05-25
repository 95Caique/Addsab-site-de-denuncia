from django import forms
from django.contrib.auth.models import User
from .models import Perfil


class LoginForm(forms.Form):
    username = forms.CharField(
        label='CPF',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite apenas números',
            'id': 'cpf'
        })
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha',
            'id': 'password'
        })
    )

class EditarUsuarioForm(forms.ModelForm):
    foto = forms.ImageField(required=False, label='Foto de Perfil')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit)
        if 'foto' in self.cleaned_data:
            user.perfil.foto = self.cleaned_data['foto']
            if commit:
                user.perfil.save()
        return user