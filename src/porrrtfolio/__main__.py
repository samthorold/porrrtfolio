import logging

from porrrtfolio.cli import cli
from porrrtfolio.services import AlphaVantage


logging.basicConfig(level="INFO")

av = AlphaVantage()

symbol = "0P000159K7"
exchange = "LSE"

# ts = av.time_series_daily_adjusted(
#     symbol=symbol,
#     exchange=exchange,
# )

# names = av.symbol_search("HSBC FTSE")

cli()
