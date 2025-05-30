from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'adm'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='adm/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='adm:login'), name='logout'),
    path('cadastrar-usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('editar-usuario/<str:username>/', views.editar_usuario, name='editar_usuario'),

    path('painel/', views.painel_adm, name='painel_adm'),

    path('esqueceu-senha/', views.CustomPasswordResetView.as_view(), name='esqueceu_senha'),
    path('senha-reset-done/', views.CustomPasswordResetDoneView.as_view(), name='senha_reset_done'),
    path('redefinir-senha/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='redefinir_senha'),
    path('senha-reset-complete/', views.CustomPasswordResetCompleteView.as_view(), name='senha_reset_complete'),
]
