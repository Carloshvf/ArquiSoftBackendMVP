# Restaurantes Favoritos — API (Back-End)

API REST desenvolvida em **Flask** para o MVP de arquitetura de software da pós-graduação. É responsável por persistir os restaurantes favoritados pelo usuário (nota pessoal, comentários e tags) e por consultar a **Overpass API (OpenStreetMap)** para descobrir restaurantes próximos a uma coordenada.

Este componente é a API secundária da arquitetura, consumida pelo Front-End em React: [https://github.com/Carloshvf/ArquiSoftFrontendMVP].

> A documentação completa da API externa utilizada (licença, cadastro, rotas consumidas) está no README do repositório principal (front-end), conforme os requisitos do projeto.

## Observações sobre a API externa

O servidor público da Overpass API (`overpass-api.de`) apresenta instabilidade ocasional, podendo retornar erros temporários (ex.: `406`, `504`, timeout) mesmo com a requisição correta. Isso é uma limitação conhecida do serviço gratuito, não do código da aplicação. Se a rota `GET /api/descobrir` falhar, repetir a requisição normalmente resolve — a API já trata esses erros retornando um `502` com uma mensagem clara em vez de quebrar a aplicação.

Caso a instabilidade persista, um mirror alternativo pode ser usado trocando a constante `OVERPASS_URL` em `app/external_api.py` para `https://overpass.kumi.systems/api/interpreter`.

## Tecnologias

- Python 3.12
- Flask + [flask-openapi3](https://luolingchun.github.io/flask-openapi3/) (Swagger automático)
- SQLAlchemy + SQLite
- Requests (consumo da API externa)
- Docker

## Rotas disponíveis

| Método | Rota                             | Descrição                                    |
| ------ | -------------------------------- | -------------------------------------------- |
| GET    | `/api/favoritos`                 | Lista os restaurantes favoritos              |
| GET    | `/api/favoritos/<id>`            | Detalha um favorito                          |
| POST   | `/api/favoritos`                 | Adiciona um restaurante aos favoritos        |
| PUT    | `/api/favoritos/<id>`            | Atualiza nota, comentário ou tags            |
| DELETE | `/api/favoritos/<id>`            | Remove um favorito                           |
| GET    | `/api/descobrir?lat=&lng=&raio=` | Busca restaurantes próximos via Overpass API |

A documentação interativa (Swagger UI) fica disponível em `/openapi` após subir a aplicação.

## Estrutura de pastas

\```
ArquiSoftBackendMVP/
├── app/
│ ├── **init**.py # application factory
│ ├── database.py # configuração do SQLAlchemy
│ ├── models.py # modelo RestauranteFavorito
│ ├── schemas.py # schemas Pydantic (validação/Swagger)
│ ├── routes.py # rotas da API
│ └── external_api.py # integração com a Overpass API
├── app.py # ponto de entrada
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md
\```

## Como rodar localmente (sem Docker)

1. Crie e ative um ambiente virtual:

python -m venv venv
venv\Scripts\Activate.ps1

2. Instale as dependências:

pip install -r requirements.txt

3. Rode a aplicação:

python app.py

4. A API estará disponível em `http://127.0.0.1:5000` e o Swagger em `http://127.0.0.1:5000/openapi`.

## Como rodar com Docker

1. Construa a imagem:

docker build -t restaurantes-backend .

2. Rode o container:

docker run -p 5000:5000 --name restaurantes-container restaurantes-backend

3. Acesse `http://127.0.0.1:5000/openapi` para testar todas as rotas.
