# 🏫 OSGADE — Sistema de Cadastro

Sistema de cadastro e gestão das crianças atendidas pela **Obra Social Gabriel Delanne**, com controle de acesso por tipo de usuário, histórico de alterações e backup de dados.

---

## 🧱 Tecnologias

| Camada         | Tecnologia                          |
|----------------|--------------------------------------|
| Backend        | Python 3.12 + Flask                  |
| Banco de dados | PostgreSQL (hospedado no [Neon](https://neon.tech)) |
| ORM            | SQLAlchemy + Flask-Migrate (Alembic) |
| Autenticação   | Flask-Login                          |
| Formulários    | Flask-WTF (com proteção CSRF)        |
| Upload de fotos| Cloudinary                           |
| Hospedagem     | [Render](https://render.com)         |
| Servidor WSGI  | Gunicorn                             |

---

## 📁 Estrutura do projeto


```
creche-ong/
│
├── app/
│ ├── init.py # cria e configura o Flask (db, login, csrf...)
│ ├── decorators.py # @admin_required (protege rotas só de admin)
│ ├── forms.py # todos os formulários (cadastro, login, usuários)
│ ├── utils.py # compressão/upload de imagens pro Cloudinary
│ │
│ ├── models/
│ │ └── init.py # tabelas do banco: Crianca, Familiar, Usuario, Historico
│ │
│ ├── routes/
│ │ ├── auth.py # login / logout
│ │ ├── criancas.py # cadastro, consulta, edição das crianças
│ │ ├── admin.py # gestão de usuários + popular banco (teste)
│ │ └── relatorios.py # estatísticas e relatórios
│ │
│ ├── static/
│ │ ├── css/ # estilos extras
│ │ └── img/ # logo da OSGADE
│ │
│ └── templates/
│ ├── shared/
│ │ └── base.html # layout base (menu, cabeçalho, rodapé)
│ ├── auth/
│ │ └── login.html # tela de login
│ ├── admin/
│ │ └── usuarios.html # gerenciar usuários (só admin)
│ ├── criancas/ # cadastro (3 etapas), busca, detalhe
│ └── relatorios/
│ └── index.html
│
├── migrations/ # histórico de mudanças no banco (Alembic)
├── config.py # configurações gerais (lê variáveis de ambiente)
├── init_db.py # cria as tabelas e o 1º usuário admin ao iniciar
├── run.py # ponto de entrada da aplicação
├── render.yaml # configuração de deploy no Render
├── requirements.txt # bibliotecas Python usadas
├── runtime.txt # versão do Python
├── Procfile # comando de start (compatibilidade)
├── .env.example # modelo das variáveis de ambiente
└── README.md
```


---

## ✅ Funcionalidades

### Cadastro de crianças
Formulário em 3 etapas: dados pessoais → familiares/responsáveis → documentos (fotos enviadas direto pro Cloudinary, comprimidas automaticamente).

### Consulta e busca
Lista de crianças com busca por nome e filtro por turno (manhã/tarde/integral).

### Relatórios
Estatísticas gerais: total por turno, faixa etária, aniversariantes do mês, alergias/problemas de saúde, documentos pendentes, etc.

### Login e permissões
O sistema exige login para tudo. Existem dois tipos de conta:

| | **Administradora** | **Funcionária** |
|---|---|---|
| Cadastrar criança nova | ✅ | ❌ |
| Editar dados/saúde/familiares | ✅ | ❌ |
| Ver telefone dos familiares | ✅ | ✅ |
| Ver alergias / problemas de saúde | ✅ | ✅ |
| Ver CPF | ✅ | ❌ |
| Ver documentos (RG, matrícula, comprovantes) | ✅ | ❌ |
| Gerenciar usuários | ✅ | ❌ |

### Histórico de alterações
Toda vez que uma admin cadastra ou edita algo em uma criança, fica registrado quem fez e quando — visível na página de detalhes.

---

## 👤 Como criar um novo usuário

1. Faça login com uma conta **administradora**
2. Vá em **Usuários** no menu lateral
3. Preencha nome, usuário, senha e o tipo de acesso (**Admin** ou **Funcionária**)
4. Clique em **Criar usuário**

Contas podem ser desativadas a qualquer momento na mesma tela, sem precisar apagar o histórico da pessoa.

---

## ☁️ Hospedagem

O sistema roda de graça em duas partes:

- **[Render](https://render.com)** → hospeda a aplicação Flask (o site)
- **[Neon](https://neon.tech)** → hospeda o banco de dados PostgreSQL

O deploy é automático: qualquer alteração enviada para a branch `main` no GitHub atualiza o site sozinha, através do `render.yaml`.

### Variáveis de ambiente necessárias (configuradas no Render)

| Variável | Descrição |
|---|---|
| `DATABASE_URL` | Connection string do banco no Neon |
| `SECRET_KEY` | Chave secreta do Flask (gerada automaticamente) |
| `ADMIN_EMAIL` / `ADMIN_SENHA` | Login e senha do primeiro usuário admin (criado automaticamente no 1º deploy) |
| `CLOUDINARY_CLOUD_NAME` | Nome da conta no Cloudinary |
| `CLOUDINARY_API_KEY` | Chave da API do Cloudinary |
| `CLOUDINARY_API_SECRET` | Segredo da API do Cloudinary |

---

## 💾 Backup dos dados

O Neon guarda automaticamente as últimas **6 horas** de alterações (restauração rápida em caso de erro), mas isso não substitui um backup de verdade.

Recomenda-se rodar periodicamente uma exportação dos dados e guardar em local seguro (Google Drive, por exemplo), usando o **SQL Editor** do Neon ou uma ferramenta de exportação em CSV.

---

## 🖥️ Rodando localmente (desenvolvimento)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # preencher com seus dados locais
python init_db.py
python run.py
