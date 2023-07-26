# ʕ •́؈•̀) `URL-shortener`

## 🔋 Getting Started

This template is meant to be used with [Poetry](https://github.com/python-poetry/poetry). If you are not familiar with this type of tool, the documentation can be found [here](https://python-poetry.org/docs/basic-usage/). To start, go through [the installation process](https://python-poetry.org/docs/#installation).

### 🌱 🛠️ Environment setup

After cloning the repo, install dependencies (`poetry install`) and spawn your shell inside of venv (`poetry shell`), copy dev env variables (`cp .env.example .env`), create postgresql database (`docker-compose up -d`) and run migrations (`alembic upgrade head`). Afterwards run the project (`poe dev`).

To reset database use `alembic downgrade base`

### 👩 💻 Developing

[`src/routes`](src/routes) should contain route functions appropriate to their filenames. Tests should be placed in [`tests`](tests).

### 🧪 Testing

This template comes with pytest example tests. To run tests use `poe test`. Some tests use locally spun-up services (DBs, brokers, etc). Before running tests, make sure that you've set up a database and run migrations with seeded data (`alembic -x seed=true upgrade head`).

### ✏️ Formatting

This template uses [`flake8`](https://github.com/PyCQA/flake8) for linting and [`black`](https://github.com/psf/black) for formatting the project.
To invoke, run `poe format` or `poe lint`. Before further development, you should install pre-commit hooks using `poe precommit`.

## 📡 🔓 HTTP status codes
In order to communicate with front-end efficiently, we need to return HTTP status code which correspondences to what happend on server after receiving a request. Stick to the conventions introduced below, please 🙏.

| HTTP status code | When to use | `aiohttp.web_exceptions` |
| --- | --- | --- |
| OK (`200`) | none of the cases below appears and everything goes as expected | `HTTPOk` |
| Created (`201`) | everything goes well and a new record is inserted into database | `HTTPCreated` |
| Bad request (`400`) | request is not in a proper format (e.g. we want json and get something else), data is incomplete (e.g. field `username` is missing), field doesn't fit expectations (e.g. `email` doesn't pass email regex check or `age` is negative) | `HTTPBadRequest` |
| Unauthorized (`401`) | request is type of authorization attempt (e.g. user tries to sign in using login and password, OAuth 2.0 token exchange/refreshment) and the attempt fails due to wrong credentials | `HTTPUnauthorized` |
| Forbidden (`403`) | request requires to be authorized, however no authorization data is provided (e.g. `Authorization` header is missing), request requires to be authorized, but authorization data is wrong (e.g. `Authorization` header includes expired token), authorization data is correct, but user simply doesn't have access to resources due to the system design | `HTTPForbidden` |
| NotFound (`404`) | request is getting some resource by ID or requires some other resources specified in request in order to execute properly, but the resource/resources cannot be found in the database (e.g. getting `user` with ID `5` but it doesn't exist) | `HTTPNotFound` |
| Conflict (`409`) | request tries to create a new record in the database with data that should be unique in table and already exists (e.g. registration endpoint gets field `username: john`, but there is already an account using this username) | `HTTPConflict` |

