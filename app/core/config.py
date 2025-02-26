from contextlib import suppress
from datetime import timedelta
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, AnyUrl, Field
from pydantic_settings import BaseSettings
from typing_extensions import TypedDict
from yaml import safe_load

semver_re = (
    r'^(0|[1-9]\d*)\.(0|[1-9]\d*)'
    r'\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)'
    r'(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+'
    r'(?:\.[0-9a-zA-Z-]+)*))?$'
)


class Server(TypedDict):
    url: str
    description: str


class OpenAPITag(TypedDict):
    name: str
    description: str


class Contact(TypedDict):
    name: str
    email: str
    url: AnyUrl


class AppConfigSchema(BaseModel):
    title: str
    debug: bool
    env: str
    service_name: str
    servers: list[Server]
    openapi_tags: list[OpenAPITag]
    contact: Contact
    root_path: str = ''


class DocsConfigSchema(BaseModel):
    openapi_url: str = '/openapi.json'
    docs_url: str = '/docs'
    redoc_url: str = '/redoc'
    description: str


class PasswordGeneratorSchema(BaseModel):
    alphabet: str
    length: int


class JWTConfigSchema(BaseSettings):
    algorithms: list[str]
    access_token_exp_delta: timedelta


class ConfigSchema(BaseSettings):
    app: AppConfigSchema
    jwt: JWTConfigSchema
    docs: DocsConfigSchema
    password_generator: PasswordGeneratorSchema


class EnvSecrets(BaseSettings):
    class Config:
        env_file = '.env'

    VERSION: str = Field('0.0.0', pattern=semver_re)
    DB_DSN: str | None = None
    API_ROOT_PATH: str = ''
    JWT_SECRET_KEY: str = 'secret-key'
    JWT_TOKEN_EXP_TIME: str = '30d'
    JWT_ALGORITHMS: list[str] = ['HS256']
    DOMAIN: str = 'http://localhost:8000'


@lru_cache
def get_config() -> ConfigSchema:
    config_paths = [
        Path('app/config.yaml'),
        Path('/src/app/config.yaml'),
    ]
    for config_path in config_paths:
        with suppress(FileNotFoundError), config_path.open() as config_file:
            config_parsed = safe_load(config_file)
            return ConfigSchema.parse_obj(config_parsed)
    raise RuntimeError('Config not found')  # pragma: no cover


config = get_config()
env_secrets = EnvSecrets()
