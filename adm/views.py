from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.contrib import messages
from comum.models import Denuncia

def is_gerente(user):
    return user.is_authenticated and user.groups.filter(name='Gerente').exists()

def is_atendente(user):
    return user.is_authenticated and user.groups.filter(name='Atendente').exists()

@user_passes_test(is_gerente)
def cadastrar_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        tipo = request.POST.get('tipo')  # 'gerente' ou 'atendente'
        if username and password and tipo:
            user = User.objects.create_user(username=username, password=password)
            grupo = Group.objects.get(name='Gerente' if tipo == 'gerente' else 'Atendente')
            user.groups.add(grupo)
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('adm:cadastrar_usuario')
        else:
            messages.error(request, 'Preencha todos os campos.')
    return render(request, 'adm/cadastrar_usuario.html')

@login_required
def painel_adm(request):
    user = request.user
    if is_gerente(user):
        denuncias = Denuncia.objects.all()
    elif is_atendente(user):
        denuncias = Denuncia.objects.filter(status='recebida') | Denuncia.objects.filter(atendente_responsavel=user)
    else:
        denuncias = Denuncia.objects.none()
    return render(request, 'adm/painel_adm.html', {'denuncias': denuncias})