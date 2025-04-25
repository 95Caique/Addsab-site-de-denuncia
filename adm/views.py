from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm

def login_view(request):
    form = LoginForm(request.POST or None)
    error_message = None

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'home')  # Redireciona para a URL de destino ou para 'home'
                return redirect(next_url)
            else:
                error_message = 'CPF ou senha inválidos. Tente novamente.'

    context = {'form': form, 'error_message': error_message}
    return render(request, 'login.html', context)
