from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils import timezone
from functools import wraps
from datetime import timedelta
from .models import Aluno, Turma, Circulacao, Ocorrencia, Frequencia, Perfil


def home_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "core/home.html")


# MUDANCA 1: user_role agora aceita perfil_escolhido como parametro
# para que o superuser possa assumir qualquer perfil
def user_role(user, perfil_escolhido=None):
    if user.is_superuser:
        return perfil_escolhido if perfil_escolhido else "direcao"
    try:
        return user.perfil.tipo
    except Perfil.DoesNotExist:
        return None


# MUDANCA 2: role_required agora le o perfil_ativo da sessao para superuser
# em vez de fixar sempre como "direcao"
def role_required(*allowed_roles):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if request.user.is_superuser:
                role = request.session.get("perfil_ativo", "direcao")
            else:
                role = user_role(request.user)
            if role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return redirect("dashboard")
        return wrapped
    return decorator


def login_view(request):
    perfis_login = [
        ("direcao", "Direcao"),
        ("professor", "Professor"),
        ("monitor", "Monitor"),
        ("responsavel", "Responsavel"),
    ]
    perfis_validos = {p[0] for p in perfis_login}

    if request.method == "GET" and not request.GET.get("perfil"):
        return render(request, "core/select_role.html", {"perfis_login": perfis_login})

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        perfil_escolhido = request.POST.get("perfil")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if perfil_escolhido not in perfis_validos:
                return render(
                    request,
                    "core/login.html",
                    {
                        "erro": "Selecione um tipo de acesso.",
                        "perfis_login": perfis_login,
                        "username": username,
                        "perfil_escolhido": perfil_escolhido,
                    },
                )

            # MUDANCA 3: superuser pula a verificacao de perfil e pode entrar em qualquer tipo
            # usuarios normais continuam sendo validados normalmente
            if not user.is_superuser:
                perfil_real = user_role(user)
                if perfil_real != perfil_escolhido:
                    return render(
                        request,
                        "core/login.html",
                        {
                            "erro": "Tipo de acesso nao corresponde ao usuario informado.",
                            "perfis_login": perfis_login,
                            "username": username,
                            "perfil_escolhido": perfil_escolhido,
                        },
                    )

            login(request, user)
            # MUDANCA 4: salva o perfil escolhido na sessao
            # context_processors e role_required vao ler daqui
            request.session["perfil_ativo"] = perfil_escolhido
            return redirect("dashboard")
        else:
            return render(
                request,
                "core/login.html",
                {
                    "erro": "Usuario ou senha incorretos",
                    "perfis_login": perfis_login,
                    "username": username,
                    "perfil_escolhido": perfil_escolhido,
                },
            )

    perfil_escolhido = request.GET.get("perfil")
    if perfil_escolhido not in perfis_validos:
        return render(request, "core/select_role.html", {"perfis_login": perfis_login})

    return render(
        request,
        "core/login.html",
        {"perfis_login": perfis_login, "perfil_escolhido": perfil_escolhido},
    )


def logout_view(request):
    logout(request)
    return redirect("login")


@role_required("direcao", "professor", "monitor", "responsavel")
def dashboard(request):
    hoje = timezone.now().date()
    periodo = request.GET.get("periodo", "dia")

    fora_de_sala = Circulacao.objects.filter(retorno__isnull=True).count()
    total_alunos = Aluno.objects.count()
    limite_alerta = timezone.now() - timedelta(minutes=5)

    if periodo == "semana":
        inicio = hoje - timedelta(days=6)
        ocorrencias_qs = Ocorrencia.objects.filter(data__range=[inicio, hoje])
        periodo_label = "na semana"
    elif periodo == "mes":
        inicio = hoje.replace(day=1)
        ocorrencias_qs = Ocorrencia.objects.filter(data__range=[inicio, hoje])
        periodo_label = "no mes"
    else:
        periodo = "dia"
        ocorrencias_qs = Ocorrencia.objects.filter(data=hoje)
        periodo_label = "hoje"

    ocorrencias_periodo = ocorrencias_qs.count()

    circulacoes_ativas = (
        Circulacao.objects
        .filter(retorno__isnull=True)
        .select_related("aluno", "aluno__turma")
        .order_by("saida")[:5]
    )
    circulacoes_em_alerta = (
        Circulacao.objects
        .filter(retorno__isnull=True, saida__lte=limite_alerta)
        .select_related("aluno", "aluno__turma")
        .order_by("saida")
    )
    ocorrencias_recentes = (
        ocorrencias_qs
        .select_related("aluno")
        .order_by("-data", "-id")[:5]
    )

    return render(request, "core/dashboard.html", {
        "fora_de_sala": fora_de_sala,
        "ocorrencias_hoje": ocorrencias_periodo,
        "total_alunos": total_alunos,
        "circulacoes_ativas": circulacoes_ativas,
        "circulacoes_em_alerta": circulacoes_em_alerta,
        "ocorrencias_recentes": ocorrencias_recentes,
        "periodo": periodo,
        "periodo_label": periodo_label,
        "active_page": "dashboard",
    })


@role_required("direcao", "professor", "monitor")
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


@role_required("direcao", "professor", "monitor")
@require_POST
def circulacao_retorno(request, pk):
    circulacao = get_object_or_404(Circulacao, pk=pk)
    circulacao.retorno = timezone.now()
    circulacao.save()
    return redirect("circulacao")


@role_required("direcao", "professor", "monitor")
@require_POST
def circulacao_alerta(request, pk):
    circulacao = get_object_or_404(Circulacao, pk=pk)
    circulacao.alerta_enviado = True
    circulacao.save()
    return JsonResponse({"status": "ok"})


@role_required("direcao", "professor", "monitor")
def alunos_por_turma(request, turma_id):
    alunos = (
        Aluno.objects
        .filter(turma_id=turma_id)
        .order_by("numero_chamada")
        .values("id", "nome", "numero_chamada")
    )
    return JsonResponse(list(alunos), safe=False)


@role_required("direcao")
def turma_list(request):
    turmas = Turma.objects.all().order_by("-ano", "serie", "tipo")
    return render(request, "core/turmas/list.html", {"turmas": turmas, "active_page": "turmas"})


@role_required("direcao")
def turma_create(request):
    if request.method == "POST":
        Turma.objects.create(
            serie=request.POST.get("serie"),
            tipo=request.POST.get("tipo"),
            ano=request.POST.get("ano"),
        )
        return redirect("turma_list")

    return render(
        request,
        "core/turmas/form.html",
        {"series": Turma.SERIES, "tipos": Turma.TIPOS, "turma": None, "active_page": "turmas"},
    )


@role_required("direcao")
def turma_edit(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    if request.method == "POST":
        turma.serie = request.POST.get("serie")
        turma.tipo = request.POST.get("tipo")
        turma.ano = request.POST.get("ano")
        turma.save()
        return redirect("turma_list")

    return render(
        request,
        "core/turmas/form.html",
        {"series": Turma.SERIES, "tipos": Turma.TIPOS, "turma": turma, "active_page": "turmas"},
    )


@role_required("direcao")
@require_POST
def turma_delete(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    turma.delete()
    return redirect("turma_list")


@role_required("direcao")
def aluno_list(request):
    alunos = (
        Aluno.objects.select_related("turma", "responsavel")
        .all()
        .order_by("turma__ano", "turma__serie", "numero_chamada")
    )
    return render(request, "core/alunos/list.html", {"alunos": alunos, "active_page": "alunos"})


@role_required("direcao")
def aluno_create(request):
    if request.method == "POST":
        Aluno.objects.create(
            nome=request.POST.get("nome"),
            turma_id=request.POST.get("turma"),
            numero_chamada=request.POST.get("numero_chamada"),
        )
        return redirect("aluno_list")

    turmas = Turma.objects.all().order_by("-ano", "serie")
    return render(request, "core/alunos/form.html", {"aluno": None, "turmas": turmas, "active_page": "alunos"})


@role_required("direcao")
def aluno_edit(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == "POST":
        aluno.nome = request.POST.get("nome")
        aluno.turma_id = request.POST.get("turma")
        aluno.numero_chamada = request.POST.get("numero_chamada")
        aluno.save()
        return redirect("aluno_list")

    turmas = Turma.objects.all().order_by("-ano", "serie")
    return render(request, "core/alunos/form.html", {"aluno": aluno, "turmas": turmas, "active_page": "alunos"})


@role_required("direcao")
@require_POST
def aluno_delete(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    aluno.delete()
    return redirect("aluno_list")


@role_required("direcao", "professor", "monitor")
def ocorrencia_list(request):
    ocorrencias = (
        Ocorrencia.objects.select_related("aluno", "turma", "registrado_por")
        .all()
        .order_by("-data", "-id")
    )
    return render(
        request,
        "core/ocorrencias/list.html",
        {"ocorrencias": ocorrencias, "active_page": "ocorrencias"},
    )


@role_required("direcao", "professor", "monitor")
def ocorrencia_create(request):
    if request.method == "POST":
        aluno = get_object_or_404(Aluno, pk=request.POST.get("aluno"))
        Ocorrencia.objects.create(
            aluno=aluno,
            turma=aluno.turma,
            descricao=request.POST.get("descricao"),
            tipo=request.POST.get("tipo"),
            gravidade=request.POST.get("gravidade"),
            local=request.POST.get("local"),
            registrado_por=request.user,
        )
        return redirect("ocorrencia_list")

    turmas = Turma.objects.all().order_by("-ano", "serie")
    return render(
        request,
        "core/ocorrencias/form.html",
        {
            "ocorrencia": None,
            "turmas": turmas,
            "tipos": Ocorrencia.TIPOS,
            "gravidades": Ocorrencia.GRAVIDADE,
            "locais": Ocorrencia.LOCAL,
            "active_page": "ocorrencias",
        },
    )


@role_required("direcao", "professor", "monitor")
def ocorrencia_edit(request, pk):
    ocorrencia = get_object_or_404(Ocorrencia, pk=pk)
    if request.method == "POST":
        aluno = get_object_or_404(Aluno, pk=request.POST.get("aluno"))
        ocorrencia.aluno = aluno
        ocorrencia.turma = aluno.turma
        ocorrencia.descricao = request.POST.get("descricao")
        ocorrencia.tipo = request.POST.get("tipo")
        ocorrencia.gravidade = request.POST.get("gravidade")
        ocorrencia.local = request.POST.get("local")
        ocorrencia.notificacao = request.POST.get("notificacao") == "on"
        ocorrencia.save()
        return redirect("ocorrencia_list")

    turmas = Turma.objects.all().order_by("-ano", "serie")
    alunos = Aluno.objects.filter(turma=ocorrencia.turma).order_by("numero_chamada")
    return render(
        request,
        "core/ocorrencias/form.html",
        {
            "ocorrencia": ocorrencia,
            "turmas": turmas,
            "alunos": alunos,
            "tipos": Ocorrencia.TIPOS,
            "gravidades": Ocorrencia.GRAVIDADE,
            "locais": Ocorrencia.LOCAL,
            "active_page": "ocorrencias",
        },
    )


@role_required("direcao", "professor", "monitor")
@require_POST
def ocorrencia_delete(request, pk):
    ocorrencia = get_object_or_404(Ocorrencia, pk=pk)
    ocorrencia.delete()
    return redirect("ocorrencia_list")


@role_required("direcao", "professor")
def frequencia_view(request):
    turmas = Turma.objects.all().order_by("-ano", "serie")
    turma_id = request.GET.get("turma")
    turma_selecionada = None
    alunos = []
    registros_presenca = []
    justificativas = {}
    hoje = timezone.now().date()

    if turma_id:
        turma_selecionada = get_object_or_404(Turma, pk=turma_id)
        alunos = Aluno.objects.filter(turma=turma_selecionada).order_by("numero_chamada")

        freq_queryset = Frequencia.objects.filter(turma=turma_selecionada, data=hoje)
        registros_presenca = [f.aluno_id for f in freq_queryset if f.presente]
        justificativas = {f.aluno_id: (f.justificativa or "") for f in freq_queryset}

    if request.method == "POST":
        turma_selecionada = get_object_or_404(Turma, pk=request.POST.get("turma"))
        alunos = Aluno.objects.filter(turma=turma_selecionada).order_by("numero_chamada")
        presentes_ids = {int(i) for i in request.POST.getlist("presentes")}

        for aluno in alunos:
            frequencia = Frequencia.objects.filter(
                aluno=aluno,
                turma=turma_selecionada,
                data=hoje,
            ).first()

            if frequencia:
                frequencia.presente = aluno.id in presentes_ids
                frequencia.justificativa = request.POST.get(f"just_{aluno.id}", "").strip()
                frequencia.save()
            else:
                Frequencia.objects.create(
                    aluno=aluno,
                    turma=turma_selecionada,
                    presente=aluno.id in presentes_ids,
                    justificativa=request.POST.get(f"just_{aluno.id}", "").strip(),
                )

        return redirect(f"{request.path}?turma={turma_selecionada.id}")

    return render(
        request,
        "core/frequencia/list.html",
        {
            "turmas": turmas,
            "turma_selecionada": turma_selecionada,
            "alunos": alunos,
            "registros_presenca": registros_presenca,
            "justificativas": justificativas,
            "hoje": hoje,
            "active_page": "frequencia",
        },
    )