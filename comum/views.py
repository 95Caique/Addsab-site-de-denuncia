from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.utils import timezone

from .forms import DenunciaForm
from .models import Denuncia, Tratativa
from .enums import STATUS_DENUNCIA_CHOICES

def denuncia_create_view(request):
    if request.method == "POST":
        form = DenunciaForm(request.POST, request.FILES)
        if form.is_valid():
            denuncia = form.save()
            messages.success(request, "Obrigado pela sua denúncia! Ela foi registrada com sucesso e será analisada pela nossa equipe.")
            # Limpa o formulário após o envio bem-sucedido
            form = DenunciaForm()
        else:
            # Adiciona mensagens de erro mais detalhadas
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erro no campo {field}: {error}")
    else:
        form = DenunciaForm()

    return render(request, "formulario_denuncia.html", {"form": form})


def lista_denuncias(request):
    # Obtém todas as denúncias ordenadas pela data de criação (mais recentes primeiro)
    denuncias = Denuncia.objects.all().order_by('-data_denuncia')
    return render(request, 'lista_denuncias.html', {'denuncias': denuncias})

# @login_required
def painel_denuncias(request):
    # Processar ações de atualização de status, atribuição ou exclusão
    if request.method == 'POST':
        action = request.POST.get('action')
        denuncia_id = request.POST.get('denuncia_id')
        
        if action and denuncia_id:
            try:
                denuncia = Denuncia.objects.get(id=denuncia_id)
                
                if action == 'update_status':
                    status_anterior = denuncia.status
                    new_status = request.POST.get('status')
                    descricao = request.POST.get('descricao', '')
                    
                    if new_status in [choice[0] for choice in STATUS_DENUNCIA_CHOICES]:
                        denuncia.status = new_status
                        denuncia.save()
                        
                        # Registra a tratativa
                        Tratativa.objects.create(
                            denuncia=denuncia,
                            # atendende=request.user --mudar quando a criação de usuario estiver ok
                            atendente=request.user if request.user.is_authenticated else None,
                            descricao=descricao,
                            status_anterior=status_anterior,
                            status_novo=new_status
                        )
                        
                        messages.success(request, f"Status da denúncia #{denuncia_id} atualizado para {denuncia.get_status_display()}.")
                
                elif action == 'atribuir':
                    atendente_id = request.POST.get('atendente_id')
                    if atendente_id:
                        atendente = User.objects.get(id=atendente_id)
                        denuncia.atribuir_atendente(atendente)
                        messages.success(request, f"Denúncia #{denuncia_id} atribuída para {atendente.get_full_name() or atendente.username}.")
                
                elif action == 'remover_atribuicao':
                    denuncia.remover_atendente()
                    messages.success(request, f"Atribuição da denúncia #{denuncia_id} removida.")
                
                elif action == 'delete':
                    denuncia.delete()
                    messages.success(request, f"Denúncia #{denuncia_id} excluída com sucesso.")
            
            except Denuncia.DoesNotExist:
                messages.error(request, f"Denúncia #{denuncia_id} não encontrada.")
            except User.DoesNotExist:
                messages.error(request, "Atendente não encontrado.")
    
    # Filtrar denúncias por status, se especificado
    status_filter = request.GET.get('status')
    atendente_filter = request.GET.get('atendente')
    
    denuncias = Denuncia.objects.all()
    
    if status_filter:
        denuncias = denuncias.filter(status=status_filter)
    if atendente_filter:
        if atendente_filter == 'sem_atendente':
            denuncias = denuncias.filter(atendente_responsavel__isnull=True)
        else:
            denuncias = denuncias.filter(atendente_responsavel_id=atendente_filter)
    
    denuncias = denuncias.order_by('-data_denuncia')

    # Lista de atendentes para o formulário de atribuição
    atendentes = User.objects.filter(is_staff=True).order_by('first_name', 'username')

    context = {
        'denuncias': denuncias,
        'processando_count': Denuncia.objects.filter(status='processando').count(),
        'recebidas_count': Denuncia.objects.filter(status='recebida').count(),
        'tratadas_count': Denuncia.objects.filter(status='tratada').count(),
        'canceladas_count': Denuncia.objects.filter(status='cancelada').count(),
        'status_choices': STATUS_DENUNCIA_CHOICES,
        'current_status': status_filter,
        'atendentes': atendentes,
        'current_user': request.user
    }

    return render(request, 'painel_denuncias.html', context)

def denuncia_detail_view(request, pk):
    denuncia = get_object_or_404(Denuncia, pk=pk)
    tratativas = Tratativa.objects.filter(denuncia=denuncia)
    context = {
        'denuncia': denuncia,
        'tratativas': tratativas,
        'status_choices': STATUS_DENUNCIA_CHOICES,
        'atendentes': User.objects.filter(is_staff=True).order_by('first_name', 'username')
    }
    return render(request, 'denuncia_detail.html', context)