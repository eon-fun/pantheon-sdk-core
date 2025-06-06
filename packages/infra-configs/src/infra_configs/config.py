from functools import lru_cache

from cryptography.fernet import Fernet
from dotenv import load_dotenv
from pydantic import Field, RedisDsn, SecretStr, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class InfrastructureConfig(BaseSettings):
    postgres_user: str = "rag"
    postgres_password: str = "rag"
    postgres_db: str = "rag"
    # postgres_user: str = "postgres"
    # postgres_password: str = "postgres"
    # postgres_db: str = "postgres"
    postgres_host: str = Field(default="localhost", validation_alias="POSTGRES_HOST")
    postgres_port: int = 5432
    postgres_logs: bool = False

    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: str = "0"

    postgres_dsn: str | None = None
    redis_dsn: RedisDsn | None = None
    fernet_key: bytes = b"glEo_3r7sSMy8tIxqRyvwLW0CrKD44ADJ7qIgWVeOOI="

    # S3 storage
    s3_bucket_prefix: str = "pantheon"
    s3_region: str = Field(validation_alias="S3_REGION")
    s3_access_key: str = Field(validation_alias="S3_ACCESS_KEY")
    s3_secret_key: str = Field(validation_alias="S3_SECRET")

    kafka_host: str = "localhost"
    kafka_port: int = 9092

    QDRANT_HOST: str = Field(default="qdrant", validation_alias="QDRANT_HOST")
    QDRANT_PORT: int = 6333

    LANGFUSE_SECRET_KEY: SecretStr = ""
    LANGFUSE_PUBLIC_KEY: SecretStr = ""

    @property
    def qdrant_url(self) -> str:
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"

    @field_validator("postgres_dsn", mode="before")
    @classmethod
    def get_postgres_dsn(cls, _, info: ValidationInfo):
        return f"postgresql+asyncpg://{info.data['postgres_user']}:{info.data['postgres_password']}@{info.data['postgres_host']}:{info.data['postgres_port']}/{info.data['postgres_db']}"
        # return PostgresDsn.build(
        #     scheme='postgresql+asyncpg',
        #     username=info.data['postgres_user'],
        #     password=info.data['postgres_password'],
        #     host=info.data['postgres_host'],
        #     port=info.data['postgres_port'],
        #     path=info.data['postgres_db'],
        # )

    @field_validator("redis_dsn", mode="before")
    @classmethod
    def get_redis_dsn(cls, _, info: ValidationInfo):
        return RedisDsn.build(
            scheme="redis",
            host=info.data["redis_host"],
            port=info.data["redis_port"],
            path=info.data["redis_db"],
        )

    @property
    def s3_base_url(self):
        return f"https://{self.s3_region}.digitaloceanspaces.com"


class TelegramAppSetupServiceConfig(BaseSettings):
    base_url: str = "https://my.telegram.org"
    send_password_endpoint: str = "/auth/send_password"
    login_endpoint: str = "/auth/login"
    app_endpoint: str = "/apps"
    create_endpoint: str = "/apps/create"

    class Config:
        env_prefix = "TELEGRAM_"


class DeployService(BaseSettings):
    host: str = Field(default="deploy-service.pantheon.svc.cluster.local")
    port: int = Field(default=80)
    connect_timeout: int = Field(default=10)
    timeout: int = Field(default=300)

    @property
    def url(self) -> str:
        return f"http://{self.host}"


class Settings(BaseSettings):
    infrastructure: InfrastructureConfig = InfrastructureConfig()
    telegram_config: TelegramAppSetupServiceConfig = TelegramAppSetupServiceConfig()
    ambassador_username: str = "testandoo6"
    CREATE_POST_INTERVAL: int = 60 * 60 * 4
    GORILLA_MARKETING_INTERVAL: int = 60 * 60 * 4
    COMMENT_AGIX_INTERVAL: int = 60 * 60 * 4
    ANSWER_DIRECT_INTERVAL: int = 60 * 60 * 4
    ANSWER_COMMENT_INTERVAL: int = 60 * 60 * 4
    ANSWER_MY_COMMENT_INTERVAL: int = 60 * 4
    LIKES_INTERVAL: int = 6 * 60 * 60
    PARTNERSHIP_INTERVAL: int = 12 * 60 * 60
    INVEST_TWEET_INTERVAL: int = 15 * 60
    TWITTER_CLIENT_ID: str = "eG8wX3VEcVdtcnZyNnhEQ3ZUbTU6MTpjaQ"
    TWITTER_CLIENT_SECRET: str = "8noXqU32HCtbW-0VIB2bw42Q_ZRdAliBYTq3BAV0nQvwhOTCux"
    TWITTER_BASIC_BEARER_TOKEN: str = "AAAAAAAAAAAAAAAAAAAAAALFxQEAAAAAteK66aMgMrX%2BoWlqS1nuVBbo834%3DKvDbzJWyE0X6hea56JtvXGPvu58wP31Tym00sFi68RKJ9OqLfj"

    TWITTER_REDIRECT_URI: str = "http://185.53.46.123:3001/api/oauth/twitter/callback"
    OPENAI_API_KEY: str = "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"
    OPEN_AI_MODEL: str = "gpt-4o-2024-08-06"
    LOGS_DIR: str = "../logs"
    TWEETSCOUT_API_KEY: str = "a6660542-6baf-4ae4-9d3d-5f564f73cb5b"
    ANTHROPIC_API_KEY: str = "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"

    HEYGEN_API_KEY: str = "Mjg4YTg5MWI2ZmEyNDIxNmI0YmQ5YjMzYmMyZDQ2MmItMTczODIzMDkxMw=="

    LIVEKIT_URL: str = "wss://streamingavatar-o51wm8kk.livekit.cloud"
    LIVEKIT_API_KEY: str = "APIqYdobFVHDpjs"
    LIVEKIT_API_SECRET: str = "y5vXmQbuNM8XCd0LE5HtIQ17aT6o2jTKb9fBqeRXGcl"

    TWITCH_CLIENT_ID: str = "d39qf2fhjamywvevtsctdxnrflma20"
    TWITCH_CLIENT_SECRET: str = "51fkl9bclgwamyfot69wlcrnkz1ajq"

    AVATAR_INTERNAL_REDIS_HOST: str = "localhost"
    AVATAR_INTERNAL_REDIS_PORT: int = 6379

    # FAL AI
    fal_ai_api_key: str = ""

    # SIWE
    domain: str = "localhost"
    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    jwt_access_token_expires_in: int = 1440

    # Creativity
    creativity_api_id: str = Field(validation_alias="CREATIVITY_API_ID")
    creativity_api_key: str = Field(validation_alias="CREATIVITY_API_KEY")
    creativity_base_url: str = "https://api.creatify.ai/api"

    # confluent_api_key: str = '1'
    # confluent_api_secret: str = '1'
    # confluent_bootstrap_server: str = '1'
    # confluent_rest_endpoint: str = '1'

    AI_REGISTRY_HOST: str = Field(
        default="pantheon-dev-ai-registry.pantheon.svc.cluster.local"
    )
    AI_REGISTRY_PORT: int = Field(default=8080)

    deploy_service: DeployService = DeployService()

    @property
    def ai_registry_url(self) -> str:
        return f"http://{self.AI_REGISTRY_HOST}:{self.AI_REGISTRY_PORT}"


class InterfaceSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class CoingeckoSettings(InterfaceSettings):
    api_key: str = Field(validation_alias="COINGECKO_API_KEY")
    base_url: str = Field(validation_alias="COINGECKO_API_URL")


class RedisSettings(InterfaceSettings):
    redis_host: str = Field(validation_alias="REDIS_HOST")
    redis_port: int = Field(validation_alias="REDIS_PORT")
    redis_db: int = Field(validation_alias="REDIS_DB")


class HyperLiquidSettings(InterfaceSettings):
    base_url: str = Field(validation_alias="HYPERLIQUD_API_URL")


class ServerSettings(InterfaceSettings):
    coingecko: CoingeckoSettings = CoingeckoSettings()
    redis: RedisSettings = RedisSettings()
    hyperliquid: HyperLiquidSettings = HyperLiquidSettings()

    REDIS_PERSONA_KEY: str = "available_personas"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore


server = ServerSettings()
cipher = Fernet(get_settings().infrastructure.fernet_key)
