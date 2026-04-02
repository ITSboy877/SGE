<h1 align="center">
  <br>
  SGE — Sistema de Gestão Escolar
  <br>
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14-blue?style=flat-square&logo=python" />
  <img src="https://img.shields.io/badge/Django-6.0.3-green?style=flat-square&logo=django" />
  <img src="https://img.shields.io/badge/Bootstrap-5.3-purple?style=flat-square&logo=bootstrap" />
  <img src="https://img.shields.io/badge/Railway-Hospedagem-black?style=flat-square&logo=railway" />
  <img src="https://img.shields.io/badge/Status-Em%20desenvolvimento-yellow?style=flat-square" />
</p>

<p align="center">
  Aplicação web para digitalizar e centralizar a gestão escolar de instituições de ensino brasileiras.
</p>

---

## Sobre o Projeto

O SGE é um sistema desenvolvido como TCC (Trabalho de Conclusão de Curso) que busca substituir processos manuais ainda presentes em muitas escolas brasileiras — como cadernos de ocorrências físicos, bilhetes impressos e registros em papel — por uma plataforma digital integrada, moderna e acessível de qualquer dispositivo.

O sistema possui controle de acesso por perfil de usuário, onde cada tipo (Direção, Professor, Monitor e Responsável) enxerga apenas as funcionalidades que lhe cabem.

---

## Funcionalidades

- **Controle de Circulação** — registro de saída de alunos com timer automático de 5 minutos, alerta visual, sonoro e notificação para monitores e direção
- **Livro de Ocorrências Digital** — registro de ocorrências com tipo, gravidade, local e histórico por aluno
- **Chamada Eletrônica** — registro de frequência diária por turma com suporte a justificativa de faltas
- **Dashboard Inteligente** — indicadores em tempo real com filtro por Hoje, Semana ou Mês; alunos em circulação e alunos que excederam o limite de tempo
- **Controle de Acesso por Perfil** — cada perfil acessa apenas o que é permitido, tanto no menu quanto nas rotas

---

## Perfis de Usuário

| Perfil | Acesso |
|--------|--------|
| **Direção** | Acesso completo: Dashboard, Circulação, Ocorrências, Chamada, Alunos e Turmas |
| **Professor** | Dashboard, Circulação, Ocorrências e Chamada |
| **Monitor** | Dashboard, Circulação e Ocorrências |
| **Responsável** | Apenas Dashboard |

> O superusuário criado via `createsuperuser` pode escolher qualquer um dos 4 perfis na tela de login e terá exatamente as permissões daquele perfil.

---

## Tecnologias

- **Back-end:** Python 3.14 + Django 6.0.3
- **Front-end:** Bootstrap 5.3 + Bootstrap Icons 1.11 + JavaScript vanilla
- **Banco de dados:** SQLite (desenvolvimento) / PostgreSQL (produção)
- **Hospedagem:** Railway (planejado)
- **Admin:** Django Jazzmin (tema Cosmo)

---

## Estrutura do Projeto

```
SGE/
├── sge/
│   ├── core/
│   │   ├── migrations/
│   │   ├── templates/
│   │   │   └── core/
│   │   │       ├── alunos/
│   │   │       │   ├── form.html
│   │   │       │   └── list.html
│   │   │       ├── frequencia/
│   │   │       │   └── list.html
│   │   │       ├── ocorrencias/
│   │   │       │   ├── form.html
│   │   │       │   └── list.html
│   │   │       ├── turmas/
│   │   │       │   ├── form.html
│   │   │       │   └── list.html
│   │   │       ├── base.html
│   │   │       ├── circulacao.html
│   │   │       ├── dashboard.html
│   │   │       ├── home.html
│   │   │       ├── login.html
│   │   │       └── select_role.html
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── context_processors.py
│   │   ├── models.py
│   │   ├── urls.py (em sge/sge/urls.py)
│   │   └── views.py
│   └── sge/
│       ├── settings.py
│       ├── urls.py
│       ├── asgi.py
│       └── wsgi.py
└── manage.py
```

---

## Models

| Model | Descrição | Campos principais |
|-------|-----------|-------------------|
| `Turma` | Turmas do Fundamental II ao Médio/Técnico | serie, tipo, ano |
| `Aluno` | Cadastro de alunos vinculados a turmas | nome, numero_chamada, turma, responsavel |
| `Ocorrencia` | Registro disciplinar | tipo, gravidade, local, descricao, data, notificacao |
| `Circulacao` | Controle de saída e retorno com timer | saida, retorno, alerta_enviado |
| `Frequencia` | Chamada eletrônica diária | presente, justificativa, data |
| `Perfil` | Tipo de perfil do usuário | tipo (direcao/professor/monitor/responsavel) |
| `Notificacao` | Histórico de notificações | tipo, mensagem, lida, data |

---

## Rotas

| Rota | Descrição |
|------|-----------|
| `/` | Dashboard (redireciona para login se não autenticado) |
| `/home/` | Tela inicial de apresentação |
| `/login/` | Seleção de perfil + formulário de login |
| `/dashboard/` | Painel principal |
| `/circulacao/` | Controle de saída e retorno de alunos |
| `/ocorrencias/` | Listagem e registro de ocorrências |
| `/frequencia/` | Chamada eletrônica por turma |
| `/alunos/` | CRUD de alunos (somente Direção) |
| `/turmas/` | CRUD de turmas (somente Direção) |
| `/admin/` | Painel administrativo Django Jazzmin |

---

## Como rodar localmente

```bash
# Clone o repositório
git clone https://github.com/ITSboy877/SGE.git
cd SGE/sge

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate     # Linux/Mac
venv\Scripts\activate        # Windows (PowerShell)
source venv/Scripts/activate # Windows (Git Bash)

# Instale as dependências
pip install django django-jazzmin

# Rode as migrations
python manage.py migrate

# Crie um superusuário
python manage.py createsuperuser

# Suba o servidor
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/login/`

> Na tela de login, escolha qualquer perfil — o superusuário tem acesso a todos eles.

---

## Status do Desenvolvimento

- [x] Models e banco de dados (7 models)
- [x] Sistema de autenticação com seleção de perfil
- [x] Controle de acesso por perfil (Direção, Professor, Monitor, Responsável)
- [x] Layout base com Bootstrap 5 — sidebar condicional por perfil, topbar, cards
- [x] Dashboard com filtro Hoje / Semana / Mês
- [x] Alunos em circulação (tempo real) e alunos que excederam o limite
- [x] Módulo de circulação com timer de 5 minutos e alertas visuais/sonoros
- [x] Módulo de ocorrências (CRUD completo)
- [x] Módulo de chamada/frequência por turma
- [x] CRUD de alunos e turmas
- [x] Admin customizado com Django Jazzmin
- [x] Select dinâmico turma → aluno via AJAX
- [ ] Dashboard personalizado para Responsável
- [ ] Notificações push para responsáveis
- [ ] Importação de alunos via planilha Excel
- [ ] Deploy no Railway com PostgreSQL

---

## Autor

**Guilherme H. A. Ribeiro**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Guilherme%20Ribeiro-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/guilherme-ribeiro-040906364)
[![GitHub](https://img.shields.io/badge/GitHub-ITSboy877-black?style=flat-square&logo=github)](https://github.com/ITSboy877)

---

<p align="center">Desenvolvido como TCC — Técnico em Desenvolvimento de Sistemas</p>
