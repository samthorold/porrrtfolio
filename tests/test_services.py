import json
from typing import Any

import pytest

from porrrtfolio.services import AlphaVantage, Requests, Response


RESPONSE_DATA_AND_ERR = Response(
    data={"a": 1},
    err={"b": 2},
)


RESPONSE_ERR = Response(
    data=None,
    err={"b": 2},
)


RESPONSE_DATA = Response(
    data={"a": 1},
    err=None,
)


@pytest.mark.parametrize(
    "resp,incl_all,exp",
    (
        (RESPONSE_DATA_AND_ERR, True, {"data": {"a": 1}, "err": {"b": 2}}),
        (RESPONSE_DATA_AND_ERR, False, {"err": {"b": 2}}),
        (RESPONSE_DATA, True, {"data": {"a": 1}, "err": None}),
        (RESPONSE_DATA, False, {"data": {"a": 1}}),
        (RESPONSE_ERR, True, {"data": None, "err": {"b": 2}}),
        (RESPONSE_ERR, False, {"err": {"b": 2}}),
    )
)
def test_response_to_dict(resp: Response, incl_all: bool, exp: dict[str, Any]) -> None:
    """Expected behaviours

    - By default, data and err attributes returned
    - Otherwise, err if present else data
    """
    assert resp.to_dict(incl_all=incl_all) == exp


@pytest.mark.parametrize(
    "resp,incl_all,exp",
    (
        (RESPONSE_DATA_AND_ERR, True, {"data": {"a": 1}, "err": {"b": 2}}),
        (RESPONSE_DATA_AND_ERR, False, {"err": {"b": 2}}),
        (RESPONSE_DATA, True, {"data": {"a": 1}, "err": None}),
        (RESPONSE_DATA, False, {"data": {"a": 1}}),
        (RESPONSE_ERR, True, {"data": None, "err": {"b": 2}}),
        (RESPONSE_ERR, False, {"err": {"b": 2}}),
    )
)
def test_response_to_json(resp: Response, incl_all: bool, exp: dict[str, Any]) -> None:
    """Expected behaviours

    - By default, data and err attributes returned
    - Otherwise, err if present else data
    """
    assert resp.to_json(incl_all=incl_all) == json.dumps(exp)


def test_requests_sad_url() -> None:
    resp = Requests().request("get", "sad url")
    assert resp.err
    assert not resp.data


@pytest.mark.network
@pytest.mark.av
def test_av_resp_err() -> None:
    """Expected behaviours

    - Bad call, e.g. no api key, to
    [`AlphaVantage.symbol_search`][porrrtfolio.services.AlphaVantage]
    returns a [`Response`][porrrtfolio.services.response]
    with an error.
    """

    av = AlphaVantage(key="")

    resp = av.symbol_search("IBM")

    assert not resp.data
    assert resp.err


@pytest.mark.network
@pytest.mark.av
def test_av_symbol_search() -> None:
    """Expected behaviours

    - Standard call to
    [`AlphaVantage.symbol_search`][porrrtfolio.services.AlphaVantage]
    returns something sensible.
    """

    av = AlphaVantage()

    resp = av.symbol_search("IBM")

    assert resp.data
    assert not resp.err


@pytest.mark.network
@pytest.mark.av
def test_av_time_series() -> None:
    """Expected behaviours

    - Standard call to
    [`AlphaVantage.time_series_daily_adjusted`][porrrtfolio.services.AlphaVantage]
    returns something sensible.
    """

    av = AlphaVantage()

    resp = av.time_series_daily_adjusted(symbol="IBM")
    breakpoint()
    assert resp.data
    assert not resp.err
