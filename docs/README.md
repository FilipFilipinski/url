# Some useful commands

### Alembic

```
alembic upgrade head # Creation of databases
alembic -x seed=true upgrade head # Creation of databases with seed

alembic downgrade base # Removal of all databases
```

### Database connection

```
.env

DATABASE_URL="DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5432/postgres"
```

### Auth

```
headers={
    "Authorization": "Bearer {TOKEN}
    }
```
