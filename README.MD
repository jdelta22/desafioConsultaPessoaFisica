# Consulta Pessoa Física API

API REST desenvolvida com Python, Django e Django REST Framework para consulta de dados de pessoas físicas por CPF através da integração com um serviço externo.

## Funcionalidades

- Consulta de pessoa física por CPF.
- Validação de parâmetros de entrada.
- Tratamento de erros e respostas padronizadas.
- Integração com API externa.
- Documentação automática via Swagger/OpenAPI.

## Tecnologias Utilizadas

- Python
- Django
- Django REST Framework
- drf-spectacular
- SQLite

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

Execute as migrações:

```bash
python manage.py migrate
```

Inicie o servidor:

```bash
python manage.py runserver
```

## Documentação da API

Após iniciar a aplicação, a documentação estará disponível em:

```text
/api/docs/
```

## Exemplo de Requisição

### Consultar Pessoa Física

```http
GET /consulta/?cpf=12345678900
```

### Exemplo de Resposta

```json
{
  "nome": "João da Silva",
  "cpf": "12345678900",
  "situacao": "Regular"
}
```

## Conceitos Praticados

- Desenvolvimento de APIs REST com Django REST Framework
- Consumo de APIs externas
- Serializers e validações
- Tratamento de exceções
- Documentação com OpenAPI/Swagger
- Organização de projetos Django

## Autor

João Pedro Calaça Costa
