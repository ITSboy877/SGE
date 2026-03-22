from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils import timezone
from .models import Aluno, Turma, Circulacao


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "core/login.html", {"erro": "Usuário ou senha incorretos"})
    return render(request, "core/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    from .models import Aluno, Circulacao, Ocorrencia
    from django.utils import timezone

    hoje = timezone.now().date()

    fora_de_sala = Circulacao.objects.filter(retorno__isnull=True).count()
    ocorrencias_hoje = Ocorrencia.objects.filter(data=hoje).count()
    total_alunos = Aluno.objects.count()

    circulacoes_ativas = (
        Circulacao.objects
        .filter(retorno__isnull=True)
        .select_related("aluno", "aluno__turma")
        .order_by("saida")[:5]
    )
    ocorrencias_recentes = (
        Ocorrencia.objects
        .filter(data=hoje)
        .select_related("aluno")
        .order_by("-id")[:5]
    )

    return render(request, "core/dashboard.html", {
        "fora_de_sala": fora_de_sala,
        "ocorrencias_hoje": ocorrencias_hoje,
        "total_alunos": total_alunos,
        "circulacoes_ativas": circulacoes_ativas,
        "ocorrencias_recentes": ocorrencias_recentes,
    })


@login_required
def circulacao_view(request):
    if request.method == "POST":
        aluno_id = request.POST.get("aluno")
        aluno = get_object_or_404(Aluno, pk=aluno_id)

        ja_fora = Circulacao.objects.filter(aluno=aluno, retorno__isnull=True).exists()
        if not ja_fora:
            Circulacao.objects.create(aluno=aluno, registrado_por=request.user)

        return redirect("circulacao")

    turmas = Turma.objects.all().order_by("serie")

    circulacoes_ativas = (
        Circulacao.objects
        .filter(retorno__isnull=True)
        .select_related("aluno", "aluno__turma")
        .order_by("saida")
    )

    return render(request, "core/circulacao.html", {
        "turmas": turmas,
        "circulacoes_ativas": circulacoes_ativas,
    })


@login_required
@require_POST
def circulacao_retorno(request, pk):
    circulacao = get_object_or_404(Circulacao, pk=pk)
    circulacao.retorno = timezone.now()
    circulacao.save()
    return redirect("circulacao")


@login_required
@require_POST
def circulacao_alerta(request, pk):
    circulacao = get_object_or_404(Circulacao, pk=pk)
    circulacao.alerta_enviado = True
    circulacao.save()
    return JsonResponse({"status": "ok"})


@login_required
def alunos_por_turma(request, turma_id):
    alunos = (
        Aluno.objects
        .filter(turma_id=turma_id)
        .order_by("numero_chamada")
        .values("id", "nome", "numero_chamada")
    )
    return JsonResponse(list(alunos), safe=False)