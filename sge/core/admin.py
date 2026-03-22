from django.contrib import admin
from .models import Turma, Aluno, Ocorrencia, Circulacao, Frequencia, Perfil, Notificacao


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ("serie", "tipo", "ano")
    ordering = ("serie",)


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("numero_chamada", "nome", "turma")
    list_filter = ("turma",)
    ordering = ("turma", "numero_chamada")
    search_fields = ("nome",)


@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ("aluno", "tipo", "gravidade", "data", "registrado_por")
    list_filter = ("tipo", "gravidade", "turma")
    ordering = ("-data",)


@admin.register(Circulacao)
class CirculacaoAdmin(admin.ModelAdmin):
    list_display = ("aluno", "saida", "retorno", "alerta_enviado", "registrado_por")
    list_filter = ("alerta_enviado",)
    ordering = ("-saida",)


@admin.register(Frequencia)
class FrequenciaAdmin(admin.ModelAdmin):
    list_display = ("aluno", "turma", "data", "presente")
    list_filter = ("turma", "presente")
    ordering = ("-data",)


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ("destinatario", "tipo", "lida", "data")
    list_filter = ("tipo", "lida")
    ordering = ("-data",)


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("usuario", "tipo")
    list_filter = ("tipo",)