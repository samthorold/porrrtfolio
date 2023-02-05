import pandas as pd


def parse_hloc(
    d: dict,
    overall_key: str | None = "Time Series (Daily)",
    column: str = "5. adjusted close",
    index_as_datetime: bool = True,
) -> pd.DataFrame:
    d = d if overall_key is None else d[overall_key]
    df = pd.DataFrame(d)
    ts = pd.to_numeric(df.T[column])
    if index_as_datetime:
        ts.index = pd.to_datetime(ts.index)
    ts = ts.sort_index()
    return ts
