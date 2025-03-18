from django.shortcuts import render, redirect
from .forms import DenunciaForm

def denuncia_create_view(request):
    if request.method == "POST":
        form = DenunciaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("denuncia_sucesso")  # Criar uma página de sucesso
    else:
        form = DenunciaForm()

    return render(request, "formulario_denuncia.html", {"form": form})