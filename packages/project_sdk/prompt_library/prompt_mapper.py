from enum import Enum
from project_sdk.prompt_library.tokens import (
    HISTORICAL_PRICE_ANALYZE, COMPLEX_ANALYZE
)


class PromptMapper(Enum):
    HISTORICAL_PRICE_ANALYZE: str = HISTORICAL_PRICE_ANALYZE
    COMPLEX_ANALYZE: str = COMPLEX_ANALYZE