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
]
