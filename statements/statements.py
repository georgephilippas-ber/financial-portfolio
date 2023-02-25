from __future__ import annotations
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass

from faker import Faker
from datetime import datetime, timedelta


def to_periods(periods: List[Tuple[int, int]]) -> List[Tuple[datetime, timedelta]]:
    def to_period(timestamp: int, days: int) -> Tuple[datetime, timedelta]:
        return datetime.fromtimestamp(timestamp), timedelta(days=days)

    return [to_period(period[0], period[1]) for period in periods]


@dataclass(frozen=True)
class Income:
    period: List[Tuple[datetime, timedelta]]
    currency: str
    currency_exponent: int

    revenues: List[float]
    COGS: List[float]
    SGA: List[float]
    operating_income: List[float]
    depreciation: List[float]
    interest: List[float]
    tax: List[float]

    net_income: List[float]

    @staticmethod
    def revive(object_: Dict) -> Income:
        return Income(period=to_periods(object_["period"]), currency=object_["currency"],
                      currency_exponent=object_["currency_exponent"], revenues=object_["revenues"],
                      COGS=object_["COGS"],
                      SGA=object_["SGA"],
                      operating_income=object_["operating_income"],
                      depreciation=object_["depreciation"],
                      interest=object_["interest"],
                      tax=object_["tax"],
                      net_income=object_["net_income"])

    def gross_margin(self) -> List[float]:
        return [(element[0] - element[1]) / element[0] for element in zip(self.revenues, self.COGS)]

    def net_profit_margin(self):
        return [element[0] / element[1] for element in zip(self.net_income, self.revenues)]

    def sga_to_gross_profit(self):
        return [element[0] / (element[1] - element[2]) for element in
                zip(self.SGA, self.revenues, self.COGS)]

    def depreciation_to_gross_profit(self):
        return [element[0] / (element[1] - element[2]) for element in
                zip(self.depreciation, self.revenues, self.COGS)]

    def interest_to_operating_income(self):
        return [element[0] / element[1] for element in
                zip(self.interest, self.operating_income)]


@dataclass(frozen=True)
class Balance:
    moment: List[int]
    currency: str
    currency_exponent: int

    cash: List[float]
    short_term_investments: List[float]
    marketable_securities: List[float]

    accounts_receivable: List[float]
    inventories: List[float]

    current_assets: List[float]

    PPE: List[float]
    accumulated_depreciation: List[float]

    goodwill: List[float]
    intangible_indefinite: List[float]
    intangible_definite: List[float]

    balance: List[float]

    accounts_payable: List[float]
    short_term_debt: List[float]
    accrued_income_taxes: List[float]

    current_liabilities: List[float]

    long_term_debt: List[float]

    @staticmethod
    def revive(object_: Dict[str, Any]) -> Balance:
        return Balance(**object_)

    def liquid(self) -> List[float]:
        return [sum(element) * 10.0 ** self.currency_exponent for element in
                zip(self.cash, self.short_term_investments, self.marketable_securities)]

    def assets(self) -> List[float]:
        return [10.0 ** self.currency_exponent * balance_ for balance_ in self.balance]

    def ppe_to_assets(self) -> List[float]:
        return [element[0] / element[1] for element in zip(self.PPE, self.balance)]


@dataclass(frozen=True)
class Cash:
    period: List[Tuple[datetime, timedelta]]
    currency: str
    currency_exponent: int

    CFO: List[float]
    capital_expenditure: List[float]
    debt_issuance: List[float]
    debt_payment: List[float]

    @staticmethod
    def revive(object_: Dict) -> Cash:
        return Cash(period=to_periods(object_["period"]), currency=object_["currency"],
                    currency_exponent=object_["currency_exponent"],
                    CFO=object_["CFO"],
                    capital_expenditure=object_["capital_expenditure"],
                    debt_issuance=object_["debt_issuance"],
                    debt_payment=object_["debt_payment"])

    def free_cash_flow_to_equity(self) -> List[float]:
        return [element[0] - element[1] - (element[3] - element[2]) for element in
                zip(self.CFO, self.capital_expenditure, self.debt_issuance, self.debt_payment)]


class Analysis:
    income: Income
    balance: Balance
    cash: Cash

    def __init__(self, income: Income, balance: Balance, cash: Cash):
        self.income = income
        self.balance = balance
        self.cash = cash


if __name__ == "__main__":
    cola_inc = {
        "period": [(0, 0)],
        "revenues": [43.004],
        "COGS": [18.000],
        "SGA": [12.880],
        "operating_income": [10.909],
        "depreciation": [1.260],
        "interest": [0.882],
        "tax": [2.115],
        "net_income": [9.542],
        "currency": "USD",
        "currency_exponent": 9
    }

    cola_bal = {
        "moment": 0,
        "currency": "USD",
        "currency_exponent": 9,

        "cash": [9.519],
        "short_term_investments": [1.043],
        "marketable_securities": [1.069],

        "accounts_receivable": [3.487],
        "inventories": [4.233],

        "current_assets": [22.591],

        "PPE": [9.841],
        "accumulated_depreciation": [0],

        "goodwill": [18.782],
        "intangible_indefinite": [14.214],
        "intangible_definite": [0.635],

        "balance": [92.763],

        "accounts_payable": [15.749],
        "short_term_debt": [2.742],
        "accrued_income_taxes": [1.203],

        "current_liabilities": [19.724],

        "long_term_debt": [36.377]
    }

    cola_cash = {
        "period": [(0, 0)],
        "currency": "USD",
        "currency_exponent": 9,
        "CFO": [11.018],
        "capital_expenditure": [1.484],
        "debt_issuance": [3.972],
        "debt_payment": [4.930]
    }

    inc = Income.revive(cola_inc)
    bal = Balance.revive(cola_bal)
    cas = Cash.revive(cola_cash)

    coke_analysis = Analysis(inc, bal, cas)
