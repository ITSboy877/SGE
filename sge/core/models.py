from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Turma(models.Model):
    SERIES = [
        ("fund_6", "6º Ano - Fundamental"),
        ("fund_7", "7º Ano - Fundamental"),
        ("fund_8", "8º Ano - Fundamental"),
        ("fund_9", "9º Ano - Fundamental"),
        ("med_1", "1º Ano - Médio"),
        ("med_2", "2º Ano - Médio"),
        ("med_3", "3º Ano - Médio"),
    ]
    TIPOS = [
        ("regular", "Ensino Regular"),
        ("tecnico", "Ensino Técnico"),
    ]
    serie = models.CharField(max_length=10, choices=SERIES, verbose_name="Série")
    tipo = models.CharField(max_length=10, choices=TIPOS, verbose_name="Tipo de Ensino")
    ano = models.IntegerField(verbose_name="Ano Letivo")

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"

    def __str__(self):
        return f"Turma: {self.get_serie_display()} ({self.get_tipo_display()}) - {self.ano}"


class Aluno(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="alunos", verbose_name="Turma")
    numero_chamada = models.IntegerField(verbose_name="Número de Chamada", validators=[MinValueValidator(1)])
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Responsável")

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"

    def __str__(self):
        return f"{self.nome} - {self.turma}"


class Ocorrencia(models.Model):
    TIPOS = [
        ("indisciplina", "Indisciplina"),
        ("briga", "Briga"),
        ("desrespeito", "Desrespeito"),
        ("outros", "Outros"),
    ]
    GRAVIDADE = [
        ("leve", "Leve"),
        ("moderado", "Moderado"),
        ("grave", "Grave"),
    ]
    LOCAL = [
        ("dentro", "Dentro da sala"),
        ("fora", "Fora da sala"),
    ]
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="ocorrencias", verbose_name="Aluno")
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True, verbose_name="Turma")
    descricao = models.TextField(null=True, blank=True, verbose_name="Descrição")
    tipo = models.CharField(max_length=20, choices=TIPOS, verbose_name="Tipo")
    gravidade = models.CharField(max_length=10, choices=GRAVIDADE, verbose_name="Gravidade")
    local = models.CharField(max_length=10, choices=LOCAL, verbose_name="Local")
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Registrado por")
    data = models.DateField(auto_now_add=True, verbose_name="Data")
    notificacao = models.BooleanField(default=False, verbose_name="Responsável Notificado")

    class Meta:
        verbose_name = "Ocorrência"
        verbose_name_plural = "Ocorrências"

    def __str__(self):
        return f"{self.aluno.nome} - {self.tipo} - {self.data:%d/%m/%Y}"


class Circulacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="circulacoes", verbose_name="Aluno")
    saida = models.DateTimeField(auto_now_add=True, verbose_name="Saída")
    retorno = models.DateTimeField(null=True, blank=True, verbose_name="Retorno")
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Registrado por")
    alerta_enviado = models.BooleanField(default=False, verbose_name="Alerta Enviado")

    class Meta:
        verbose_name = "Circulação"
        verbose_name_plural = "Circulações"

    def __str__(self):
        return f"{self.aluno.nome} - {self.saida:%d/%m/%Y %H:%M}"


class Frequencia(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="frequencia", verbose_name="Aluno")
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name="Turma")
    data = models.DateField(auto_now_add=True, verbose_name="Data")
    presente = models.BooleanField(default=True, verbose_name="Presente")
    justificativa = models.TextField(null=True, blank=True, verbose_name="Justificativa")

    class Meta:
        verbose_name = "Frequência"
        verbose_name_plural = "Frequências"

    def __str__(self):
        status = "Presente" if self.presente else "Ausente"
        return f"{self.aluno.nome} - {self.data:%d/%m/%Y} - {status}"


class Perfil(models.Model):
    TIPO = [
        ("professor", "Professor"),
        ("monitor", "Monitor"),
        ("direcao", "Direção"),
        ("responsavel", "Responsável"),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil", verbose_name="Usuário")
    tipo = models.CharField(max_length=15, choices=TIPO, verbose_name="Tipo de Perfil")

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_display()}"


class Notificacao(models.Model):
    TIPOS = [
        ("ocorrencia", "Ocorrência Disciplinar"),
        ("falta", "Falta"),
        ("atraso", "Atraso"),
        ("matando_aula", "Matando Aula"),
        ("acumulo_ocorrencias", "Acúmulo de Ocorrências"),
    ]
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notificacoes", verbose_name="Destinatário")
    tipo = models.CharField(max_length=20, choices=TIPOS, verbose_name="Tipo")
    mensagem = models.TextField(verbose_name="Mensagem")
    lida = models.BooleanField(default=False, verbose_name="Lida")
    data = models.DateTimeField(auto_now_add=True, verbose_name="Data")

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"

    def __str__(self):
        return f"{self.destinatario.username} - {self.tipo} - {self.data:%d/%m/%Y %H:%M}"