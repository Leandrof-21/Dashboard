#Dashboard Executivo de Vendas

Aplicação Full-Stack de dashboard executivo desenvolvida para visualização de métricas de vendas, faturamento, tickets médios, gráficos interativos por categoria e listagem com filtros dinâmicos.

##Tecnologias Utilizadas

Este projeto foi construído utilizando as seguintes tecnologias e ferramentas:

* **Backend:** Python, FastAPI, SQLAlchemy, Uvicorn, Psycopg2
* **Banco de Dados:** PostgreSQL (rodando via Docker)
* **Frontend:** HTML5, CSS3, JavaScript (Vanilla), Chart.js
* **Ferramentas:** Git, GitHub, Docker & Docker Compose

---

##Estrutura do Projeto

```text
seu-repositorio/
│
├── .venv/                  # Ambiente virtual Python (ignorado pelo git)
├── database.py             # Configuração da conexão SQLAlchemy
├── docker-compose.yml      # Configuração do container PostgreSQL
├── index.html              # Interface gráfica do Dashboard
├── init.sql                # Script SQL de criação de tabelas e carga inicial
├── main.py                 # Rotas e API FastAPI
├── script.js               # Lógica de consumo da API e gráficos (Chart.js)
├── style.css               # Estilização da interface
└── README.md               # Documentação do projeto
Como Executar o Projeto Localmente
Siga os passos abaixo para rodar o projeto na sua máquina:

1. Clonar o Repositório
Bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
2. Subir o Banco de Dados (Docker)
Certifique-se de que o Docker está aberto e execute o comando na raiz do projeto para subir o PostgreSQL:

Bash
docker compose up -d
3. Configurar o Ambiente Virtual e Dependências (Python)
Crie e ative o seu ambiente virtual:

Bash
python -m venv .venv
# No Windows:
.venv\Scripts\activate
# No Linux/Mac:
source .venv/bin/activate
Instale as dependências necessárias:

Bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary
4. Iniciar a API (FastAPI)
Inicie o servidor backend com o Uvicorn:

Bash
uvicorn main:app --reload
A API estará rodando em: http://127.0.0.1:8000

Você pode acessar a documentação interativa (Swagger) em: http://127.0.0.1:8000/docs

5. Executar o Frontend
Abra o arquivo index.html utilizando o Live Server (no VS Code) ou sirva-o através de um servidor local na porta 5500.

 Endpoints da API
GET /api/kpis — Retorna os dados consolidados (Faturamento Total, Total de Vendas e Ticket Médio).

GET /api/grafico-categorias — Retorna os rótulos e valores agrupados para o gráfico de barras.

GET /api/tabela-vendas — Retorna a listagem de vendas com suporte a paginação e filtro opcional por categoria.

Autor
Desenvolvido por Leandro de Souza Soares Filho.