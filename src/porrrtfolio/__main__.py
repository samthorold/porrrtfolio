import logging

from porrrtfolio.cli import cli
from porrrtfolio.services import AlphaVantage


logging.basicConfig(level="INFO")


av = AlphaVantage()


cli()
