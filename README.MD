# Consulta Pessoa Física API

API REST desenvolvida com **Python** e **FastAPI** para consulta de dados de pessoas físicas por CPF através da integração com um serviço externo.

## Funcionalidades

- Consulta de pessoa física por CPF.
- Validação de parâmetros de entrada.
- Tratamento de erros e respostas padronizadas.
- Integração com API externa.
- Documentação automática via OpenAPI/Swagger.

## Tecnologias Utilizadas

- Python
- FastAPI
- Playrigwht
- Uvicorn
- Pydantic
- Requests

## Instalação

Clone o repositório:

```bash
git clone <url-do-repositorio>
cd desafioConsultaPessoaFisica
```

Crie e ative um ambiente virtual:

```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Executando a Aplicação

Inicie o servidor:

```bash
uvicorn main:app --reload
```

A API estará disponível em:

```text
http://localhost:8000
```

## Documentação da API

Documentação interativa Swagger:

```text
/docs
```

Documentação ReDoc:

```text
/redoc
```

## Exemplo de Requisição

### Consultar Pessoa Física

```http
GET /consulta/?cpf=12345678900
```

## Conceitos Praticados

- Desenvolvimento de APIs REST com FastAPI
- Validação de dados com Pydantic
- Consumo de APIs externas
- Tratamento de exceções
- Documentação automática com OpenAPI
- Organização de projetos Python

## Estrutura do Projeto

```text
.
├── api/
│   └── main.py
├── scrapper.py
├── requirements.txt
└── README.md
```

## Autor

João Pedro Calaça Costa
