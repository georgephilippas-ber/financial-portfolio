from __future__ import annotations
from typing import Optional, List

from single import AssetClass, Industry, Strategy


class Asset:
    id: int
    assetClass: AssetClass
    industry: Optional[Industry]
    strategy: Optional[Strategy]

    symbol: str
    exchange: str

    def __init__(self, id_: int, symbol: str, exchange: str, asset_class: AssetClass, industry: Industry = None,
                 strategy: Strategy = None):
        self.id = id_
        self.symbol = symbol
        self.exchange = exchange
        self.assetClass = asset_class
        self.industry = industry
        self.strategy = strategy


class Position:
    pass
