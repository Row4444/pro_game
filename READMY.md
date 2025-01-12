# Setup Project

1. `cp .env.dist .env`
2. `docker compose up -d --build`
3. `docker compose exec web python manage.py migrate`


Run tests: 
`docker compose exec web pytest tests/`


#### Authorization in websockets use the Authorization: <JWToken> header without AUTH_HEADER_TYPES(Bearer)

