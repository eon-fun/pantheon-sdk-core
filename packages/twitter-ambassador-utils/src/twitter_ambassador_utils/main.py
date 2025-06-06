import asyncio
import base64
import hashlib
import os
import re
from datetime import datetime

import aiohttp
from loguru import logger
from redis_client.main import decode_redis, get_redis_db
from requests_oauthlib import OAuth2Session

from twitter_ambassador_utils.config import cipher, get_settings

settings = get_settings()


async def post_request(url: str, token: str, payload: dict):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.ok:
                data = await response.json()
                logger.info(f"Request successful: {data}")
                return data
            logger.error(
                f"Request failed. Status: {response.status}, Response: {await response.text()}"
            )
            return await response.json()


async def create_post(
    access_token: str,
    tweet_text: str,
    quote_tweet_id: str | None = None,
    commented_tweet_id: str | None = None,
) -> dict | None:
    logger.info(f"Posting tweet: {tweet_text=} {quote_tweet_id=} {commented_tweet_id=}")
    url = "https://api.x.com/2/tweets"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload: dict[str, str | dict[str, str]] = {
        "text": tweet_text,
    }
    if quote_tweet_id:
        payload.update({"quote_tweet_id": quote_tweet_id})

    if commented_tweet_id:
        payload.update({"reply": {"in_reply_to_tweet_id": commented_tweet_id}})

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 201:
                result = await response.json()
                logger.info(f"Tweet posted: {result}")
                return result
            logger.error(f"Twit not posted: {await response.text()}")
            return None


async def retweet(token: str, user_id: str, tweet_id: str):
    url = f"https://api.x.com/2/users/{user_id}/retweets"
    payload = {"tweet_id": tweet_id}
    return await post_request(url, token, payload)


async def set_like(token: str, user_id: str, tweet_id: str):
    url = f"https://api.x.com/2/users/{user_id}/likes"
    payload = {"tweet_id": tweet_id}
    return await post_request(url, token, payload)


class TwitterAuthClient:
    _CLIENT = OAuth2Session(
        client_id=settings.TWITTER_CLIENT_ID,
        redirect_uri=settings.TWITTER_REDIRECT_URI,
        scope="tweet.read users.read follows.write tweet.write like.write like.read follows.read offline.access",
    )
    _DB = get_redis_db()

    @classmethod
    def create_auth_link(cls, user_id: str = None):
        """Сохраняем API, но не используем user_id."""
        code_verifier = cls._generate_code_verifier()
        code_challenge = cls._generate_code_challenge(code_verifier)

        url, state = cls._CLIENT.authorization_url(
            url="https://twitter.com/i/oauth2/authorize",
            code_challenge=code_challenge,
            code_challenge_method="S256",
        )
        cls._store_session_data(
            session_id=state,
            data={
                "code_challenge": code_challenge,
                "code_verifier": code_verifier,
            },
            ex=60,
        )
        return url

    @classmethod
    async def callback(cls, state: str, code: str):
        """Twitter send here after user allow to connect to his account."""
        tokens_data = await cls.get_tokens(state, code)
        user_data = await cls.get_me(tokens_data["access_token"])
        cls.save_twitter_data(**tokens_data, **user_data)
        return True

    @classmethod
    async def get_tokens(cls, state: str, code: str):
        """Get tokens from state and code that twitter had sent to callback."""
        if not (data := cls.get_session_data(state)):
            return None
        loop = asyncio.get_running_loop()
        tokens_data = await loop.run_in_executor(
            None,
            lambda: cls._CLIENT.fetch_token(
                token_url="https://api.twitter.com/2/oauth2/token",
                code=code,
                client_secret=settings.TWITTER_CLIENT_SECRET,
                code_verifier=data["code_verifier"],
            ),
        )
        return {
            # Убираем user_id, который больше не нужен
            "access_token": tokens_data["access_token"],
            "refresh_token": tokens_data["refresh_token"],
            "expires_at": tokens_data["expires_at"],
        }

    @classmethod
    async def get_me(cls, access_token: str) -> dict | None:
        logger.info("Get me twitter")
        async with (
            aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=aiohttp.ClientTimeout(10),
            ) as session,
            session.get("https://api.twitter.com/2/users/me") as response,
        ):
            data = await response.json()
            if response.status == 403 and "suspended" in data["detail"]:
                response.raise_for_status()

            if not response.ok:
                logger.error(f"Bad request to twitter get_me - {data}")
                return None

            return {
                "name": data["data"]["name"],
                "username": data["data"]["username"],
                "twitter_id": data["data"]["id"],
            }

    @classmethod
    def _generate_code_verifier(cls) -> str:
        code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
        return re.sub("[^a-zA-Z0-9]+", "", code_verifier)

    @classmethod
    def _generate_code_challenge(cls, code_verifier: str) -> str:
        code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
        return code_challenge.replace("=", "")

    @classmethod
    def _store_session_data(cls, session_id: str, data: dict, ex: int) -> None:
        """Store data created with auth link in order to get it when twitter send callback."""
        cls._DB.r.hmset(f"session:{session_id}", mapping=data)
        cls._DB.r.expire(f"session:{session_id}", ex)

    @classmethod
    def get_session_data(cls, session_id: str) -> dict | None:
        if session_data := cls._DB.r.hgetall(f"session:{session_id}"):
            return decode_redis(session_data)
        return None

    @classmethod
    def save_twitter_data(
        cls,
        access_token: str,
        refresh_token: str,
        expires_at: int,
        name: str,
        username: str,
        twitter_id: str,
        user_id: str = None,
        **_,
    ):
        user_id_value = user_id if user_id is not None else twitter_id

        cls._DB.r.hmset(
            f"twitter_data:{username}",
            mapping={
                "access_token": cipher.encrypt(access_token.encode()).decode(),
                "refresh_token": cipher.encrypt(refresh_token.encode()).decode(),
                "expires_at": expires_at,
                "name": name,
                "username": username,
                "id": twitter_id,
                "user_id": user_id_value,
            },
        )

    @classmethod
    async def _refresh_tokens(cls, refresh: str):
        loop = asyncio.get_running_loop()
        tokens_data = await loop.run_in_executor(
            None,
            lambda: cls._CLIENT.refresh_token(
                token_url="https://api.twitter.com/2/oauth2/token",
                refresh_token=refresh,
                client_id=settings.TWITTER_CLIENT_ID,
                client_secret=settings.TWITTER_CLIENT_SECRET,
                headers={
                    "Authorization": f"Basic {settings.TWITTER_BASIC_BEARER_TOKEN}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            ),
        )
        return {
            "access_token": tokens_data["access_token"],
            "refresh_token": tokens_data["refresh_token"],
            "expires_at": tokens_data["expires_at"],
        }

    @classmethod
    async def update_tokens(cls, refresh_token: str, username: str):
        new_tokens = await cls._refresh_tokens(refresh_token)
        tokens_to_save = {
            "access_token": cipher.encrypt(
                new_tokens["access_token"].encode()
            ).decode(),
            "refresh_token": cipher.encrypt(
                new_tokens["refresh_token"].encode()
            ).decode(),
            "expires_at": new_tokens["expires_at"],
        }
        cls._DB.r.hmset(
            f"twitter_data:{username}",
            mapping=tokens_to_save,
        )
        return tokens_to_save

    @classmethod
    async def disconnect_twitter(cls, username: str):
        cls._DB.r.delete(f"twitter_data:{username}")

    @classmethod
    async def get_twitter_data(cls, username: str) -> dict | None:
        encoded_data = cls._DB.r.hgetall(f"twitter_data:{username}")
        decoded_data = decode_redis(encoded_data)
        if not decoded_data:
            return None
        access_token = decoded_data["access_token"]
        if (
            datetime.utcfromtimestamp(float(decoded_data.get("expires_at")))
            < datetime.utcnow()
        ):
            refresh_token = cipher.decrypt(
                decoded_data["refresh_token"].encode()
            ).decode()
            access_token = (await cls.update_tokens(refresh_token, username))[
                "access_token"
            ]
        return {
            "name": decoded_data["name"],
            "username": decoded_data["username"],
            "id": decoded_data["id"],
            "access_token": access_token,
            "auth_token": decoded_data.get("auth_token"),  # cookies
            "csrf_token": decoded_data.get("csrf_token"),  # cookies
            "guest_id": decoded_data.get("guest_id"),  # cookies
        }

    @classmethod
    def get_static_data(cls, username: str) -> dict | None:
        encoded_data = cls._DB.r.hgetall(f"twitter_data:{username}")
        decoded_data = decode_redis(encoded_data)
        return {
            "name": decoded_data["name"],
            "username": decoded_data["username"],
            "id": decoded_data["id"],
            "auth_token": decoded_data.get("auth_token"),  # cookies
            "csrf_token": decoded_data.get("csrf_token"),  # cookies
            "guest_id": decoded_data.get("guest_id"),  # cookies
        }

    @classmethod
    async def get_access_token(cls, username: str) -> str:
        twitter_data = await cls.get_twitter_data(username)
        if not twitter_data:
            logger.error(f"No twitter data found for {username}")
            raise ValueError(f"Twitter data not found for user {username}")
        try:
            access_token = cipher.decrypt(twitter_data["access_token"]).decode()
            logger.info("Decoded access token successfully")
            return access_token
        except (KeyError, TypeError) as e:
            logger.error(f"Error decrypting access token for {username}: {e}")
            raise e
