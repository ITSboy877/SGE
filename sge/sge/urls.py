from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("circulacao/", views.circulacao_view, name="circulacao"),
    path("circulacao/retorno/<int:pk>/", views.circulacao_retorno, name="circulacao_retorno"),
    path("circulacao/alerta/<int:pk>/", views.circulacao_alerta, name="circulacao_alerta"),
    path("circulacao/alunos/<int:turma_id>/", views.alunos_por_turma, name="alunos_por_turma"),
]