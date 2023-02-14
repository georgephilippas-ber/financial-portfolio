from __future__ import annotations
from typing import List, Optional


class SingleString:
    id: int
    value: str

    def __init__(self, id_: int, value: str):
        self.id = id_
        self.value = value

    def get(self):
        return self.value

    def __str__(self):
        return f"{self.id} {self.value}"


class AssetClass(SingleString):
    def __init__(self, single_string: SingleString):
        super().__init__(single_string.id, single_string.value)


class Strategy(SingleString):
    def __init__(self, single_string: SingleString):
        super().__init__(single_string.id, single_string.value)


class Industry(SingleString):
    def __init__(self, single_string: SingleString):
        super().__init__(single_string.id, single_string.value)


class SingleStringUniverse:
    universe: List[SingleString]

    def __init__(self, universe: List[SingleString]):
        self.universe = universe

    def by_id(self, id_: int) -> Optional[SingleString]:
        for singleString in self.universe:
            if singleString.id == id_:
                return singleString

        return None

    def by_value(self, value: str):
        for singleString in self.universe:
            if singleString.value == value:
                return singleString

        return None

    def __str__(self):
        return str([singleString.value for singleString in self.universe])

    @staticmethod
    def from_value_list(list_: List[str]) -> SingleStringUniverse:
        return SingleStringUniverse([SingleString(id_, value) for id_, value in enumerate(list_)])


asset_class_universe_value_list = [
    "equity", "debt", "ETF"
]

assetClassUniverse = SingleStringUniverse.from_value_list(asset_class_universe_value_list)
