from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    kafka_bootstrap_servers: str = "kafka:29092"
    database_url: str = (
        "postgresql://eaglevision:eaglevision@postgres:5432/eaglevision"
    )
    gateway_port: int = 8000
    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    model_config = {"env_prefix": "", "case_sensitive": False}


settings = Settings()
