from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.core.files.storage import default_storage


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

        if not all([username, password, tipo]):
            messages.error(request, 'Preencha todos os campos.')
            return redirect('adm:cadastrar_usuario')

        try:
            user = User.objects.create_user(username=username, password=password)
            grupo_nome = 'Gerente' if tipo == 'gerente' else 'Atendente'
            grupo, created = Group.objects.get_or_create(name=grupo_nome)
            user.groups.add(grupo)
            messages.success(request, f'Usuário {username} foi criado com sucesso!')
            return redirect('adm:painel_adm')
        except Exception as e:
            messages.error(request, f'Erro ao criar usuário: {str(e)}')
            return redirect('adm:cadastrar_usuario')

    return render(request, 'adm/cadastrar_usuario.html')


# @login_required
def editar_usuario(request, username):
    try:
        usuario = User.objects.get(username=username)

        if request.method == 'POST':
            novo_username = request.POST.get('username')
            password = request.POST.get('password')
            tipo = request.POST.get('tipo')
            foto = request.FILES.get('foto')

            if not all([novo_username, tipo]):
                messages.error(request, 'Preencha todos os campos obrigatórios.')
                return redirect('adm:editar_usuario', username=username)

            try:
                # Atualizar username se foi alterado
                if novo_username != username:
                    usuario.username = novo_username

                # Atualizar senha se fornecida
                if password:
                    usuario.set_password(password)

                # Atualizar grupo
                usuario.groups.clear()
                grupo_nome = 'Gerente' if tipo == 'gerente' else 'Atendente'
                grupo, created = Group.objects.get_or_create(name=grupo_nome)
                usuario.groups.add(grupo)

                # Atualizar foto de perfil
                if foto:
                    if hasattr(usuario, 'perfil') and usuario.perfil.foto:
                        default_storage.delete(usuario.perfil.foto.path)  # Remover foto antiga
                    usuario.perfil.foto = foto
                    usuario.perfil.save()

                usuario.save()
                messages.success(request, f'Usuário {novo_username} atualizado com sucesso!')
                return redirect('adm:painel_adm')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar usuário: {str(e)}')

        # Determinar tipo atual do usuário
        tipo_atual = 'gerente' if usuario.groups.filter(name='Gerente').exists() else 'atendente'

        context = {
            'usuario': usuario,
            'tipo_atual': tipo_atual
        }
        return render(request, 'adm/editar_usuario.html', context)

    except User.DoesNotExist:
        messages.error(request, 'Usuário não encontrado.')
        return redirect('adm:painel_adm')

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
                    msg = f'Usuário {usuario.username} foi desativado com sucesso.'
                else:  # reativar
                    usuario.is_active = True
                    msg = f'Usuário {usuario.username} foi reativado com sucesso.'

                usuario.save()
                messages.success(request, msg)

            except User.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')

    # Obter todos os usuários (excluindo superusuários)
    usuarios = User.objects.exclude(is_superuser=True)

    # Processar usuários ativos e inativos
    usuarios_info = {
        'ativos': [],
        'inativos': []
    }

    for usuario in usuarios:
        # Criar perfil se não existir
        if not hasattr(usuario, 'perfil'):
            from .models import Perfil
            Perfil.objects.create(user=usuario)

        tipo = 'Gerente' if usuario.groups.filter(name='Gerente').exists() else 'Atendente'
        usuario_info = {
            'username': usuario.username,
            'nome_completo': usuario.get_full_name() or usuario.username,
            'tipo': tipo,
            'ultimo_login': usuario.last_login,
            'data_cadastro': usuario.date_joined,
            'foto_perfil': usuario.perfil.foto.url if usuario.perfil.foto else None
        }

        status = 'ativos' if usuario.is_active else 'inativos'
        usuarios_info[status].append(usuario_info)

    context = {
        'usuarios_status': usuarios_info,
        'ativos_count': len(usuarios_info['ativos']),
        'inativos_count': len(usuarios_info['inativos'])
    }

    return render(request, 'adm/painel_adm.html', context)