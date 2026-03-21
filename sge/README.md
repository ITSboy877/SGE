<h1 align="center">
  <br>
  📚 SGE — Sistema de Gestão Escolar
  <br>
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14-blue?style=flat-square&logo=python" />
  <img src="https://img.shields.io/badge/Django-6.0.3-green?style=flat-square&logo=django" />
  <img src="https://img.shields.io/badge/Bootstrap-5-purple?style=flat-square&logo=bootstrap" />
  <img src="https://img.shields.io/badge/Railway-Hospedagem-black?style=flat-square&logo=railway" />
  <img src="https://img.shields.io/badge/Status-Em%20desenvolvimento-yellow?style=flat-square" />
</p>

<p align="center">
  Aplicação web no formato PWA para digitalizar e centralizar a gestão escolar de instituições de ensino brasileiras.
</p>

---

## 📋 Sobre o Projeto

O SGE é um sistema desenvolvido como TCC (Trabalho de Conclusão de Curso) que busca substituir processos manuais ainda presentes em muitas escolas brasileiras — como cadernos de ocorrências físicos, bilhetes impressos e registros em papel — por uma plataforma digital integrada, moderna e acessível de qualquer dispositivo.

## ✨ Funcionalidades

- 🔄 **Controle de Circulação** — registro de saída de alunos com timer automático de 5 minutos e alertas para monitores e direção
- 📋 **Livro de Ocorrências Digital** — registro de ocorrências com histórico por aluno e notificação automática aos responsáveis
- 📊 **Chamada Eletrônica** — registro de frequência com possibilidade de justificativa de faltas pelos responsáveis
- 📱 **Comunicação Escola-Família** — notificações push em tempo real para os responsáveis
- 📈 **Dashboard Inteligente** — indicadores de presença por turma, alunos fora de sala e ocorrências do período

## 👥 Perfis de Usuário

| Perfil | Permissões |
|--------|-----------|
| **Professor** | Registrar circulação, chamada e ocorrências |
| **Monitor** | Receber alertas de circulação e registrar ocorrências |
| **Direção** | Acesso completo ao sistema e relatórios |
| **Responsável** | Visualizar informações dos filhos e justificar faltas |

## 🛠️ Tecnologias

- **Back-end:** Python 3.14 + Django 6.0.3
- **Front-end:** HTML, CSS, JavaScript, Bootstrap 5
- **Banco de dados:** SQLite (desenvolvimento) / PostgreSQL (produção)
- **Hospedagem:** Railway
- **Formato:** PWA (Progressive Web App)

## 🗃️ Models

- `Turma` — séries do Fundamental II ao Ensino Médio
- `Aluno` — cadastro de alunos vinculados a turmas
- `Ocorrencia` — registro disciplinar com tipo, gravidade e local
- `Circulacao` — controle de saída e retorno de alunos
- `Frequencia` — chamada eletrônica diária
- `Perfil` — tipo de perfil de cada usuário
- `Notificacao` — histórico de notificações enviadas

## 🚀 Como rodar localmente

```bash
# Clone o repositório
git clone https://github.com/ITSboy877/SGE.git
cd SGE/sge

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install django

# Rode as migrations
python manage.py migrate

# Crie um superusuário
python manage.py createsuperuser

# Suba o servidor
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/login/`

## 📅 Status do Desenvolvimento

- [x] Models e banco de dados
- [x] Sistema de autenticação
- [ ] Interface com Bootstrap 5
- [ ] Dashboard com indicadores
- [ ] Módulo de circulação com timer
- [ ] Módulo de ocorrências
- [ ] Módulo de chamada
- [ ] Notificações push
- [ ] Importação via planilha Excel
- [ ] Deploy no Railway

## ✍️ Autor

**Guilherme H. A. Ribeiro**
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Guilherme%20Ribeiro-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/guilherme-ribeiro-040906364)
[![GitHub](https://img.shields.io/badge/GitHub-ITSboy877-black?style=flat-square&logo=github)](https://github.com/ITSboy877)

---

<p align="center">Desenvolvido com 💙 como TCC</p>
