from typing import Callable, ClassVar

from aiohttp import ClientSession
from aiohttp.client import _RequestOptions
from multidict import CIMultiDict

from shared_clients.aiohttp_.session import AiohttpSession



class TweetScoutSession(AiohttpSession):
    BASE_URL: ClassVar[str] = "https://api.tweetscout.io/v2/"

    __slots__ = ("__api_key",)

    def __init__(self, api_key: str, session_provider: Callable[[], ClientSession] | None = None) -> None:
        super().__init__(session_provider, self.BASE_URL)
        self.__api_key = api_key

    def _handle_kwargs(self, **kwargs) -> _RequestOptions:
        headers = CIMultiDict[str]()
        headers.extend(kwargs.get("headers") or {})
        headers.add("ApiKey", self.__api_key)
        kwargs["headers"] = headers

        return kwargs
