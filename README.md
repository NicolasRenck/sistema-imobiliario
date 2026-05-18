# Expert Imóveis - Sistema de Gestão

Sistema web interno para gestão de imóveis e proprietários, desenvolvido para a Expert Imóveis de Novo Hamburgo/RS. Permite que corretores cadastrem, acompanhem e gerenciem o portfólio de imóveis, com sincronização automática com Google Sheets e upload de fotos via Cloudinary.

## Demo

| | URL |
|--|--|
| **Frontend** | [sistema-imobiliario.netlify.app](https://sistema-imobiliario.netlify.app) |
| **API Docs** | [sistema-imobiliario-fv6g.onrender.com/api/docs](https://sistema-imobiliario-fv6g.onrender.com/api/docs/) |

---

## Screenshots

### Login
![Login](docs/screenshots/login.png)

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### Imóveis
![Imóveis](docs/screenshots/imoveis.png)

### Tabela com imóveis cadastrados
![Tabela](docs/screenshots/tabela.png)

### Proprietários
![Proprietários](docs/screenshots/proprietarios.png)

### Relatório de vendas
![Relatório](docs/screenshots/relatorio.png)

---

## Tecnologias

**Backend**
- Python + Django + Django REST Framework
- PostgreSQL (Neon)
- JWT Authentication (SimpleJWT)
- Google Sheets API (gspread)
- Cloudinary (armazenamento de imagens)
- Docker

**Frontend**
- HTML, CSS e JavaScript puro
- Consumo da API REST via Fetch API

**Deploy**
- Backend: Render
- Frontend: Netlify

---

## Funcionalidades

- Autenticação com JWT - login, logout com blacklist de token
- Cadastro e gestão de imóveis com múltiplas fotos
- Cadastro e gestão de proprietários
- Controle de status dos imóveis - à venda, suspenso, vendido
- Sincronização automática com Google Sheets ao cadastrar ou excluir imóvel
- Upload de fotos direto para o Cloudinary
- Filtros por status, busca por nome/endereço e ordenação
- Relatório de vendas com métricas - total vendido, volume e média
- Dashboard com visão geral do portfólio

---

## Estrutura do projeto

```
sistema-imobiliario/
├── app/
│   ├── models.py          # Proprietario, Imovel, FotoImovel
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── sheets.py          # Integração Google Sheets
├── core/
│   ├── settings.py
│   └── urls.py
├── frontend/
│   ├── index.html         # Login
│   ├── dashboard.html
│   ├── imoveis.html
│   ├── proprietarios.html
│   ├── relatorio.html
│   ├── assets/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── api.js
│       └── auth.js
├── docs/
│   └── screenshots/
├── credentials.json       # Google Sheets (não commitado)
├── .env                   # Variáveis de ambiente (não commitado)
├── netlify.toml
├── Dockerfile
├── requirements.txt
└── manage.py
```

---

## Como rodar localmente

### Pré-requisitos
- Python 3.11+
- PostgreSQL
- Conta no Neon (ou PostgreSQL local)
- Conta no Cloudinary
- Conta no Google Cloud com Sheets API ativada
- Docker (opcional)

### 1. Clone o repositório

```bash
git clone https://github.com/NicolasRenck/sistema-imobiliario.git
cd sistema-imobiliario
```

### 2. Crie o ambiente virtual e instale as dependências

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua_secret_key_aqui
DEBUG=True
DATABASE_URL=postgres://usuario:senha@host:5432/nome_do_banco
```

### 4. Configure o Google Sheets

- Crie um projeto no Google Cloud Console
- Ative a Google Sheets API
- Crie uma conta de serviço e baixe o `credentials.json`
- Coloque o `credentials.json` na raiz do projeto
- Compartilhe a planilha com o e-mail da conta de serviço

Adicione ao `settings.py`:
```python
GOOGLE_CREDENTIALS_PATH = os.path.join(BASE_DIR, 'credentials.json')
GOOGLE_SHEET_ID = 'id_da_sua_planilha'
```

### 5. Rode as migrações

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Inicie o servidor

```bash
python manage.py runserver
```

### 7. Inicie o frontend

Abra a pasta `frontend/` com o Live Server do VSCode ou rode:

```bash
cd frontend
python -m http.server 5500
```

Acesse `http://127.0.0.1:5500`

---

## Rodando com Docker

```bash
docker build -t sistema-imobiliario .
docker run -p 8000:8000 --env-file .env sistema-imobiliario
```

---

## Endpoints principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/token/` | Login |
| POST | `/api/token/refresh/` | Renovar token |
| GET/POST | `/api/imoveis/` | Listar e cadastrar imóveis |
| GET/PATCH/DELETE | `/api/imoveis/{id}/` | Detalhe, edição e exclusão |
| GET/POST | `/api/imoveis/{id}/fotos/` | Fotos do imóvel |
| GET/POST | `/api/proprietarios/` | Listar e cadastrar proprietários |
| GET/PATCH/DELETE | `/api/proprietarios/{id}/` | Detalhe, edição e exclusão |
| GET | `/api/imoveis/?status=vendido` | Relatório de vendas |
| GET | `/api/docs/` | Documentação Swagger |

---

## Variáveis de ambiente

| Variável | Descrição |
|----------|-----------|
| `SECRET_KEY` | Chave secreta do Django |
| `DEBUG` | True em desenvolvimento, False em produção |
| `DATABASE_URL` | URL de conexão com o banco PostgreSQL |
| `ALLOWED_HOSTS` | Hosts permitidos separados por vírgula |
| `GOOGLE_CREDENTIALS_PATH` | Caminho para o credentials.json |
| `GOOGLE_SHEET_ID` | ID da planilha Google Sheets |

---

## Autor

**Nicolas Renck**
- GitHub: [github.com/NicolasRenck](https://github.com/NicolasRenck)
- LinkedIn: [linkedin.com/in/nicolas-renck-75ba74232](https://linkedin.com/in/nicolas-renck-75ba74232)
- E-mail: nicolas.renck@gmail.com