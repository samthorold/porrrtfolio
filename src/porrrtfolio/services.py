import dataclasses
import os
from typing import Protocol

import requests


_AV_KEY_NAME = "PORRRTFOLIO_ALPHA_VANTAGE_KEY"


@dataclasses.dataclass
class Response:
    data: dict | None
    err: str | None

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)


class RequestMaker(Protocol):
    def request(self, method: str, url, **kwargs) -> Response:
        ...


class Requests:
    def request(self, method: str, url: str, **kwargs) -> Response:
        try:
            resp = requests.request(method=method, url=url, **kwargs)
        except Exception as err:
            return Response(err=repr(err))
        if resp.ok:
            try:
                return Response(data=resp.json())
            except Exception as err:
                return Response(err=f"Err turninging {resp.contents=} into json {repr(err)}")


class AlphaVantage:
    """Alpha Vantage API wrapper.

    The methods on this class call the endpoints available through the
    Alpha Vantage API.

    See the [Alpha Vantage](https://www.alphavantage.co/documentation/)
    docs for more info.

    """

    _base_url = "https://www.alphavantage.co/query"

    def __init__(self, key: str | None, request_maker: RequestMaker = Requests):
        self._key = key if key is not None else os.getenv(_AV_KEY_NAME)

    def time_series_daily_adjusted(self, symbol: str, exchange: str | None) -> dict:
        function = "TIME_SERIES_DAILY_ADJUSTED"
        if exchange is not None:
            symbol = f"{exchange}.{symbol}"
        resp = self.request_maker.request(
            method="GET",
            url=self._base_url,
            params={
                "function": function,
                "symbol": symbol,
                "apikey": self._key,
            }
        )

        return resp.to_dict()
