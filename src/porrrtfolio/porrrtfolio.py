"""Porrrtfolio analysis."""

import os

import requests


_BASE_URL = "https://www.alphavantage.co/query"


def daily_prices(symbol: str, exchange: str | None = None, key: str | None = None) -> dict:
    key = os.getenv("AV_KEY") if key is None else key
    if exchange:
        symbol = f"{exchange}.{symbol}"
    return requests.get(
        url=_BASE_URL,
        params={
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": symbol,
            "outputsize": "full",
            "apikey": key,
        }
    ).json()
