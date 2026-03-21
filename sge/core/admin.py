from django.contrib import admin
from .models import Turma, Aluno, Ocorrencia, Circulacao, Frequencia, Perfil, Notificacao

admin.site.register(Turma)
admin.site.register(Aluno)
admin.site.register(Ocorrencia)
admin.site.register(Circulacao)
admin.site.register(Frequencia)
admin.site.register(Perfil)
admin.site.register(Notificacao)