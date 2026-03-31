from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.dashboard, name="home"),
    path("home/", views.home_view, name="home_page"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("circulacao/", views.circulacao_view, name="circulacao"),
    path("circulacao/retorno/<int:pk>/", views.circulacao_retorno, name="circulacao_retorno"),
    path("circulacao/alerta/<int:pk>/", views.circulacao_alerta, name="circulacao_alerta"),
    path("circulacao/alunos/<int:turma_id>/", views.alunos_por_turma, name="alunos_por_turma"),

    path("turmas/", views.turma_list, name="turma_list"),
    path("turmas/nova/", views.turma_create, name="turma_create"),
    path("turmas/<int:pk>/editar/", views.turma_edit, name="turma_edit"),
    path("turmas/<int:pk>/excluir/", views.turma_delete, name="turma_delete"),

    path("alunos/", views.aluno_list, name="aluno_list"),
    path("alunos/novo/", views.aluno_create, name="aluno_create"),
    path("alunos/<int:pk>/editar/", views.aluno_edit, name="aluno_edit"),
    path("alunos/<int:pk>/excluir/", views.aluno_delete, name="aluno_delete"),

    path("ocorrencias/", views.ocorrencia_list, name="ocorrencia_list"),
    path("ocorrencias/nova/", views.ocorrencia_create, name="ocorrencia_create"),
    path("ocorrencias/<int:pk>/editar/", views.ocorrencia_edit, name="ocorrencia_edit"),
    path("ocorrencias/<int:pk>/excluir/", views.ocorrencia_delete, name="ocorrencia_delete"),

    path("frequencia/", views.frequencia_view, name="frequencia"),
]