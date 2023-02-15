from typing import Tuple, List

from dataclasses import dataclass

import requests
from requests.exceptions import RequestException

import urllib3

from typing import Any, Optional

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@dataclass(frozen=True)
class Allocation:
    cash: float
    equity: float
    fixed_income: float

    def total(self):
        return self.cash + self.equity + self.fixed_income


@dataclass(frozen=True)
class Position:
    contractId: int
    quantity: int
    currentPrice: float
    currency: str
    unrealizedPnL: float
    ticker: str
    name: str
    assetType: Tuple[str, str]


@dataclass(frozen=True)
class AccountDetails:
    accountId: str
    accountTitle: str


class InteractiveBrokersAccount:
    base_url_ = "https://localhost:5000/v1/api"

    __details: AccountDetails

    def __init__(self):
        if InteractiveBrokersAccount.__tickle() and self.__retrieve_account_details():
            print("connected")
        else:
            raise Exception("connection error")

    @staticmethod
    def __tickle() -> bool:
        try:
            return requests.post(InteractiveBrokersAccount.base_url_ + "/tickle", verify=False).status_code == 200
        except RequestException as e:
            return False

    def __retrieve_account_details(self) -> bool:
        try:
            response_ = requests.get(InteractiveBrokersAccount.base_url_ + "/portfolio/accounts", verify=False)

            if response_.status_code == 200 and len(response_.json()) > 0:
                self.__details = AccountDetails(accountId=response_.json()[0]["accountId"],
                                                accountTitle=response_.json()[0]["accountTitle"])

                return True
            else:
                print(response_.status_code)

                return False
        except RequestException as e:
            print(e)

            return False

    def allocation(self) -> Optional[Allocation]:
        try:
            response_ = requests.get(
                InteractiveBrokersAccount.base_url_ + f"/portfolio/{self.__details.accountId}/allocation",
                verify=False)

            if response_.status_code == 200:
                return Allocation(cash=response_.json()["assetClass"]["long"].get("CASH") or 0,
                                  equity=response_.json()["assetClass"]["long"].get("STK") or 0,
                                  fixed_income=response_.json()["assetClass"]["long"].get("BOND") or 0)
        except Exception as e:
            print(e)

            return None

    @staticmethod
    def __get_contract(symbol: str) -> Optional[str]:
        try:
            response_ = requests.post(InteractiveBrokersAccount.base_url_ + "/iserver/secdef/search",
                                      data={"symbol": symbol, "name": False}, verify=False)

            if response_.status_code == 200 and len(response_.json()) > 0:
                return response_.json()[0]["conid"]
            else:
                return None
        except Exception as e:
            print(e)

            return None

    def details(self) -> Optional[AccountDetails]:
        return self.__details

    def positions(self) -> Optional[List[Position]]:
        try:
            response_ = requests.get(
                InteractiveBrokersAccount.base_url_ + f"/portfolio/{self.__details.accountId}/positions/0",
                verify=False)

            if response_.status_code == 200 and type(response_.json()) == list:
                positions_ = []
                for position in response_.json():
                    positions_.append(
                        Position(position["conid"], position["position"], position["mktPrice"], position["currency"],
                                 position["unrealizedPnl"], position["ticker"], position["name"],
                                 (position["assetClass"], position["type"])))

                return positions_
            else:
                return None
        except Exception as e:
            print(e)

            return None


if __name__ == "__main__":
    pass
