from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DenunciaForm
from .models import Denuncia

def denuncia_create_view(request):
    if request.method == "POST":
        form = DenunciaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Sua denúncia foi registrada com sucesso.")
        else:
            messages.error(request, "Por favor, corrija os erros no formulário.")
    else:
        form = DenunciaForm()

    return render(request, "formulario_denuncia.html", {"form": form})