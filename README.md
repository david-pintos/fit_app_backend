# Fit App Backend

A generic REST API backend for fitness class and event management applications, built with FastAPI.

The project provides a starting point for developing customizable backend services that can be adapted to different organizations and deployment environments.

It is designed to be reusable and extensible, keeping application-specific configuration and business logic separate from the core implementation.

> **Project status:** Early development. The API, architecture and features are subject to change. This project is not yet intended for production use.

## Features

Current functionality includes:

- REST API development using FastAPI.
- Configuration management with Pydantic Settings.
- Authentication based on JSON Web Tokens (JWT).
- Password hashing and verification using pwdlib.
- Dependency-based authentication and user validation.

Additional functionality and improvements will be introduced progressively.

## Requirements

Python dependencies are declared on [pyproject.toml](/pyproject.toml) and manager through `uv`.

- Python 3.14 or later.
- FastAPI
- uv package and project management


## Getting Started


1. **Clone the repository:**

```bash
git clone https://github.com/david-pintos/fit_app_backend.git
cd fit_app_backend/
```

2. **Create the virtual environment and install dependencies:**

```bash
uv venv .venv
uv sync
```

3. **Configure environment variables:**

This project requires an environment configuration file (settings.env) which will contain all the configuration parameters, this
configuration file will be described on the next section. Once configured, it can be run with `uv` tool with the following command:

```bash
uv run fastapi dev
```

4. **Run the development server:**

Access the API on [127.0.0.1:8000](http://127.0.0.1:8000) or [127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).


## Configuration

On the previous section the configuration file has been introduced. It is consumed by the application with [pydantic-settings](https://pydantic.dev/docs/validation/latest/concepts/pydantic_settings/).
This generates an object with all configuration files, which are described on [config.py](/app/config.py):

This options must be defined on an environment script named `settings.env`, the file [settings.env.sample](/settings.env.sample) shows a configuration example file.

### Authentication parameters

| **Variable** | **Description** |
| ------------ | --------------- |
| SECRET_KEY | Secret key used to sign and verify JWT tokens. Generate a secure random value using `openssl rand -hex 32`. |
| HASH_ALGORITHM | JWT signing algorithm. The default configuration uses HS256. |
| ACCESS_TOKEN_EXPIRE_DAYS | Access token validity period, expressed in days. |

Example:

```
SECRET_KEY="test-key-example"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_DAYS=15
```

**Security considerations:**

- Use a unique, randomly generated secret key for each environment.
- Never commit real secrets or credentials to the repository.
- Do not reuse development secrets in production.
- Use HTTPS when deploying the API.
- Review authentication and authorization settings before exposing the service publicly.


## Project Structure

The project follows a modular service-oriented structure. Each application module groups the components associated with a specific domain or feature.

A simplified representation of the current structure is shown below:

```
fit_app_backend/
|---- pyproject.toml
|---- settings.env
|
|---- app/
      |---- main.py
      |---- config.py
      |---- security/
      |     |---- authentication.py
      |     |---- models.py
      |     |---- routes.py
      |---- users/
            |---- models.py
```

Each module can contain its own:

- Data models.
- Request and response schemas.
- API routes and endpoints.
- Business logic and services.

Modules exposing API endpoints must be registered in the main application through FastAPI routers (_APIRoute_).

The project structure may evolve as additional features and architectural components are introduced.

## License

This project is licensed under the **GNU General Public License v3.0**. See LICENSE file for details.
