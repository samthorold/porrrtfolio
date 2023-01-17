"""Porrrtfolio analysis."""

import json
import os
import pathlib

import requests


_BASE_URL = "https://www.alphavantage.co/query"
_DATA_DIR = pathlib.Path("data/av")


def prices(
    symbol: str,
    exchange: str | None = None,
    read_from_cache: bool = True,
    key: str | None = None,
) -> dict:
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    if exchange:
        symbol = f"{exchange}.{symbol}"
    path = pathlib.Path(f"{_DATA_DIR / symbol}.json")
    if read_from_cache:
        if path.exists():
            with open(path) as f:
                return json.load(f)
    key = os.getenv("AV_KEY") if key is None else key
    d = requests.get(
        url=_BASE_URL,
        params={
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": symbol,
            "outputsize": "full",
            "apikey": key,
        },
    ).json()
    if read_from_cache:
        with open(path, "w") as f:
            json.dump(d, f)
    return d
