from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.contrib import messages
from comum.models import Denuncia

def is_gerente(user):
    return user.is_authenticated and user.groups.filter(name='Gerente').exists()

def is_atendente(user):
    return user.is_authenticated and user.groups.filter(name='Atendente').exists()

# @user_passes_test(is_gerente)
def cadastrar_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        tipo = request.POST.get('tipo')  # 'gerente' ou 'atendente'
        if username and password and tipo:
            user = User.objects.create_user(username=username, password=password)
            grupo = Group.objects.get(name='Gerente' if tipo == 'gerente' else 'Atendente')
            user.groups.add(grupo)
            messages.success(request, f'Usuário {username} foi criado com sucesso!')
            return redirect('adm:painel_adm')
        else:
            messages.error(request, 'Preencha todos os campos.')
            return redirect('adm:cadastrar_usuario')
    return render(request, 'adm/cadastrar_usuario.html')

# @login_required
def painel_adm(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        
        if user_id and action in ['desativar', 'reativar']:
            try:
                usuario = User.objects.get(username=user_id)
                if action == 'desativar':
                    usuario.is_active = False
                    messages.success(request, f'Usuário {usuario.username} foi desativado com sucesso.')
                else:
                    usuario.is_active = True
                    messages.success(request, f'Usuário {usuario.username} foi reativado com sucesso.')
                usuario.save()
                return redirect('adm:painel_adm')
            except User.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')
                return redirect('adm:painel_adm')
    
    # Obter todos os usuários ativos e inativos
    usuarios_ativos = User.objects.filter(is_active=True).exclude(is_superuser=True)
    usuarios_inativos = User.objects.filter(is_active=False).exclude(is_superuser=True)

    # Preparar listas com informações detalhadas dos usuários
    ativos_info = []
    for usuario in usuarios_ativos:
        tipo = 'Gerente' if usuario.groups.filter(name='Gerente').exists() else 'Atendente'
        ativos_info.append({
            'username': usuario.username,
            'nome_completo': usuario.get_full_name() or usuario.username,
            'tipo': tipo,
            'ultimo_login': usuario.last_login,
            'data_cadastro': usuario.date_joined
        })

    inativos_info = []
    for usuario in usuarios_inativos:
        tipo = 'Gerente' if usuario.groups.filter(name='Gerente').exists() else 'Atendente'
        inativos_info.append({
            'username': usuario.username,
            'nome_completo': usuario.get_full_name() or usuario.username,
            'tipo': tipo,
            'ultimo_login': usuario.last_login,
            'data_cadastro': usuario.date_joined
        })

    context = {
        'usuarios_ativos': ativos_info,
        'usuarios_inativos': inativos_info,
        'ativos_count': len(ativos_info),
        'inativos_count': len(inativos_info)
    }

    return render(request, 'adm/painel_adm.html', context)