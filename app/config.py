from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Estas variáveis devem ter o mesmo nome que no ficheiro .env
    MONGODB_URI: str
    DATABASE_NAME: str

    # Configuração para ler o ficheiro .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Ignora variáveis extras no .env que não estejam definidas aqui
    )

# Cria uma instância única para ser importada em todo o projeto
settings = Settings()