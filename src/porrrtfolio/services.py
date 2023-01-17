"""Interfaces and implementations for external services."""

import dataclasses
import json
import logging
import os
from typing import Protocol

import requests


_AV_KEY_NAME = "PORRRTFOLIO_ALPHA_VANTAGE_KEY"


logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Response:
    """Response from [RequestMaker][porrrtfolio.services.RequestMaker].

    Idea is there will either be some data or an error.

    So instead of `if "err" in resp`, `if resp.err`.

    Not a massive quality of life improvement but a bit more structured.

    Methods:
        to_dict:  Response as a dictionary.
    """

    data: dict | None
    err: str | None

    def to_dict(self, incl_all: bool = True) -> dict:
        if incl_all:
            return dataclasses.asdict(self)
        if self.data:
            return self.data
        return self.err

    def to_json(self, incl_all: bool = False) -> str:
        return json.dumps(self.to_dict(incl_all=incl_all))


class RequestMaker(Protocol):
    def request(self, method: str, url, **kwargs) -> Response:
        ...


class Requests:
    def request(self, method: str, url: str, **kwargs) -> Response:
        try:
            resp = requests.request(method=method, url=url, **kwargs)
            req = resp.request
            logger.info(f"{req.url=}, {req.body=}")
        except Exception as err:
            return Response(err=repr(err), data=None)
        if resp.ok:
            try:
                data = resp.json()
            except Exception as err:
                return Response(
                    err=f"Err turning {resp.content=} into json {repr(err)}", data=None
                )
            else:
                if any("err" in k.lower() for k in data):
                    return Response(err=data, data=None)
                return Response(data=data, err=None)


class AlphaVantage:
    """Alpha Vantage API wrapper.

    The methods on this class call the endpoints available through the
    Alpha Vantage API.

    See the [Alpha Vantage](https://www.alphavantage.co/documentation/)
    docs for more info.

    """

    _base_url = "https://www.alphavantage.co/query"

    def __init__(
        self, key: str | None = None, request_maker: RequestMaker | None = None
    ):
        self._key = key if key is not None else os.getenv(_AV_KEY_NAME)
        self._request_maker = Requests() if request_maker is None else request_maker

    def time_series_daily_adjusted(self, symbol: str, exchange: str | None) -> dict:
        function = "TIME_SERIES_DAILY_ADJUSTED"
        if exchange is not None:
            symbol = f"{exchange}.{symbol}"
        resp = self._request_maker.request(
            method="GET",
            url=self._base_url,
            params={
                "function": function,
                "symbol": symbol,
                "apikey": self._key,
            },
        )
        return resp

    def symbol_search(self, keywords: str) -> dict:
        function = "SYMBOL_SEARCH"
        resp = self._request_maker.request(
            method="GET",
            url=self._base_url,
            params={"function": function, "keywords": keywords, "apikey": self._key},
        )
        return resp
