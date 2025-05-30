from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from comum.models import Denuncia

@login_required
def get_denuncias_count(request):
    """Retorna os contadores de denúncias atualizados"""
    recebidas_count = Denuncia.objects.filter(status='recebida').count()
    processando_count = Denuncia.objects.filter(status='processando').count()
    tratadas_count = Denuncia.objects.filter(status='tratada').count()
    canceladas_count = Denuncia.objects.filter(status='cancelada').count()
    
    return JsonResponse({
        'recebidas': recebidas_count,
        'processando': processando_count,
        'tratadas': tratadas_count,
        'canceladas': canceladas_count
    }) 