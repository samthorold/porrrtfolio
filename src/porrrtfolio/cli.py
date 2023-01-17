from typing import Optional
import typer

from porrrtfolio.services import AlphaVantage


cli = typer.Typer()


@cli.command()
def symbol_search(keywords: str) -> None:
    resp = AlphaVantage().symbol_search(keywords)
    print(resp.to_json())


@cli.command()
def prices(symbol: str, exchange: Optional[str] = None) -> None:
    resp = AlphaVantage().time_series_daily_adjusted(
        symbol=symbol, exchange=exchange,
    )
    print(resp.to_json())
