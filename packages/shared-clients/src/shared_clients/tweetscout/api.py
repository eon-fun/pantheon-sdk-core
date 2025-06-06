from typing import overload

from msgspec import json

from shared_clients.aiohttp_ import AiohttpAPI

from . import dto
from .session import TweetScoutSession


class TweetScoutAPI(AiohttpAPI[TweetScoutSession]):
    @overload
    async def follows(
        self, *, link: str, user_id: None = None
    ) -> list[dto.HandlerLookupRes]: ...

    @overload
    async def follows(
        self, *, link: None = None, user_id: str
    ) -> list[dto.HandlerLookupRes]: ...

    async def follows(
        self, *, link: str | None = None, user_id: str | None = None
    ) -> list[dto.HandlerLookupRes]:
        params: dict[str, str] = {}
        if link is not None:
            params["link"] = link
        elif user_id is not None:
            params["user_id"] = user_id
        async with self._session.get(url="follows", params=params) as resp:
            return json.decode(await resp.read(), type=list[dto.HandlerLookupRes])

    async def info_id(self, user_id: str) -> dto.HandlerLookupRes:
        url = f"info-id/{user_id}"
        async with self._session.get(url=url) as resp:
            return json.decode(await resp.read(), type=dto.HandlerLookupRes)

    async def info(self, user_handle: str) -> dto.HandlerLookupRes:
        url = f"info/{user_handle}"
        async with self._session.get(url=url) as resp:
            return json.decode(await resp.read(), type=dto.HandlerLookupRes)

    async def list_members(self, list_id: str) -> list[dto.HandlerListMember]:
        params = {"list_id": list_id}
        async with self._session.get(url="list-members", params=params) as resp:
            return json.decode(await resp.read(), type=list[dto.HandlerListMember])

    async def list_tweets(
        self, list_id: str, cursor: str | None = None
    ) -> dto.HandlerListTweetsRes:
        params = {"list_id": list_id}
        if cursor:
            params["cursor"] = cursor
        async with self._session.get(url="list-tweets", params=params) as resp:
            return json.decode(await resp.read(), type=dto.HandlerListTweetsRes)

    async def search_tweets(
        self, payload: dto.HandlerSearchTweetsReq
    ) -> dto.HandlerSearchTweetsRes:
        async with self._session.post(
            url="search-tweets", json=payload.to_dict()
        ) as resp:
            return json.decode(await resp.read(), type=dto.HandlerSearchTweetsRes)

    async def tweet_info(
        self, payload: dto.HandlerTweetInfoReq
    ) -> dto.HandlerTweetInfoResp:
        async with self._session.post(url="tweet-info", json=payload.to_dict()) as resp:
            return json.decode(await resp.read(), type=dto.HandlerTweetInfoResp)

    async def user_tweets(
        self, payload: dto.HandlerUserTweetsReq
    ) -> dto.HandlerUserTweetsRes:
        async with self._session.post(
            url="user-tweets", json=payload.to_dict()
        ) as resp:
            return json.decode(await resp.read(), type=dto.HandlerUserTweetsRes)

    async def handle_to_id(self, user_handle: str) -> dto.HandlerIDRes:
        url = f"handle-to-id/{user_handle}"
        async with self._session.get(url=url) as resp:
            return json.decode(await resp.read(), type=dto.HandlerIDRes)

    async def id_to_handle(self, user_id: str) -> dto.HandlerHandleRes:
        url = f"id-to-handle/{user_id}"
        async with self._session.get(url=url) as resp:
            return json.decode(await resp.read(), type=dto.HandlerHandleRes)

    @overload
    async def handle_history(
        self, *, link: str, user_id: None = None
    ) -> dto.HandlerHandleHistoriesResp: ...

    @overload
    async def handle_history(
        self, *, link: None = None, user_id: str
    ) -> dto.HandlerHandleHistoriesResp: ...

    async def handle_history(
        self, *, link: str | None = None, user_id: str | None = None
    ) -> dto.HandlerHandleHistoriesResp:
        params: dict[str, str] = {}
        if link is not None:
            params["link"] = link
        elif user_id is not None:
            params["user_id"] = user_id
        async with self._session.get(url="handle-history", params=params) as resp:
            return json.decode(await resp.read(), type=dto.HandlerHandleHistoriesResp)

    @overload
    async def followers_stats(
        self, *, user_handle: str, user_id: None = None
    ) -> dto.HandlerFollowersStatsResp: ...

    @overload
    async def followers_stats(
        self, *, user_handle: None = None, user_id: str
    ) -> dto.HandlerFollowersStatsResp: ...

    async def followers_stats(
        self, *, user_handle: str | None = None, user_id: str | None = None
    ) -> dto.HandlerFollowersStatsResp:
        params: dict[str, str] = {}
        if user_handle is not None:
            params["user_handle"] = user_handle
        elif user_id is not None:
            params["user_id"] = user_id
        async with self._session.get(url="followers-stats", params=params) as resp:
            return json.decode(await resp.read(), type=dto.HandlerFollowersStatsResp)

    @overload
    async def new_following_7d(
        self, *, user_handle: str, user_id: None = None
    ) -> list[dto.TypesFollower]: ...

    @overload
    async def new_following_7d(
        self, *, user_handle: None = None, user_id: str
    ) -> list[dto.TypesFollower]: ...

    async def new_following_7d(
        self, *, user_handle: str | None = None, user_id: str | None = None
    ) -> list[dto.TypesFollower]:
        params: dict[str, str] = {}
        if user_handle is not None:
            params["user_handle"] = user_handle
        elif user_id is not None:
            params["user_id"] = user_id
        async with self._session.get(url="new-following-7d", params=params) as resp:
            return json.decode(await resp.read(), type=list[dto.TypesFollower])

    @overload
    async def score_changes(
        self, *, user_handle: str, user_id: None = None
    ) -> dto.HandlerScoreChangesResp: ...

    @overload
    async def score_changes(
        self, *, user_handle: None = None, user_id: str
    ) -> dto.HandlerScoreChangesResp: ...

    async def score_changes(
        self, *, user_handle: str | None = None, user_id: str | None = None
    ) -> dto.HandlerScoreChangesResp:
        params: dict[str, str] = {}
        if user_handle is not None:
            params["user_handle"] = user_handle
        elif user_id is not None:
            params["user_id"] = user_id
        async with self._session.get(url="score-changes", params=params) as resp:
            return json.decode(await resp.read(), type=dto.HandlerScoreChangesResp)

    async def score_id(self, user_id: str) -> dto.HandlerScoreResp:
        url = f"score-id/{user_id}"
        async with self._session.get(url=url) as resp:
            return json.decode(await resp.read(), type=dto.HandlerScoreResp)

    async def score(self, user_handle: str) -> dto.HandlerScoreResp:
        url = f"score/{user_handle}"
        async with self._session.get(url=url) as resp:
            return json.decode(await resp.read(), type=dto.HandlerScoreResp)

    async def top_followers(
        self, user_handle: str, from_db: str | None = None
    ) -> list[dto.TypesAccount]:
        url = f"top-followers/{user_handle}"
        params: dict[str, str] = {}
        if from_db is not None:
            params["from"] = from_db
        async with self._session.get(url=url, params=params) as resp:
            return json.decode(await resp.read(), type=list[dto.TypesAccount])

    async def top_following(self, user_handle: str) -> list[dto.TypesAccount]:
        url = f"top-following/{user_handle}"
        async with self._session.get(url=url) as resp:
            return json.decode(await resp.read(), type=list[dto.TypesAccount])
