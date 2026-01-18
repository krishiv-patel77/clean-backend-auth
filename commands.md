[Alembic Commands]

### This command adds a new migration which should be done everytime there is a schema chance (think git commit)
docker-compose run backend alembic revision --autogenerate -m "New Migration"

### This command actually applies all those migrations to the database (think git push)
docker-compose run backend alembic upgrade head