from django import forms

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
