import json

import pandas as pd

from porrrtfolio import parse


with open("data/HUKX.json") as f:
    HLOC = json.load(f)


def test_parse_hloc() -> None:
    ts = parse.parse_hloc(HLOC)
    expected = pd.Series()
