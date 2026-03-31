from .models import Perfil


def perfil_context(request):
    perfil_tipo = None
    if request.user.is_authenticated:
        if request.user.is_superuser:
            perfil_tipo = request.session.get("perfil_ativo", "direcao")
        else:
            try:
                perfil_tipo = request.user.perfil.tipo
            except Perfil.DoesNotExist:
                perfil_tipo = None
    return {"perfil_tipo": perfil_tipo}