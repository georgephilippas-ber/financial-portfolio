from typing import Tuple, Optional

import json
from requests import get
from requests.exceptions import RequestException

from datetime import datetime, timedelta

TOKEN = "63ece8b64d25d2.46009852"


def write_exchanges():
    try:
        response = get(f"https://eodhistoricaldata.com/api/exchanges-list/?api_token={TOKEN}&fmt=json")

        if response.status_code == 200:
            file = open("exchanges-list.json", "w")

            file.write(json.dumps(response.json()))
            file.close()
    except RequestException as e:
        print(e)


# ticker = symbol.exchange
def latest_close(ticker: str) -> Optional[Tuple[str, float]]:
    from_: datetime = datetime.now() - timedelta(days=1)

    try:
        response = get(
            f"https://eodhistoricaldata.com/api/eod/{ticker.upper()}?api_token={TOKEN}&period=d&fmt=json&from={from_.year}-{from_.month:02}-{from_.day:02}")

        if response.status_code == 200 and type(response.json()) == list and len(response.json()) > 0:
            day_ = "today" if datetime.now().strftime("%Y-%m-%d") == response.json()[-1]["date"] else "not-today"

            return day_, response.json()[-1]["close"]
        else:
            return None
    except RequestException as e:
        print(e)

        return None


if __name__ == "__main__":
    run = False

    if run:
        print("XDDA.XETRA", latest_close("XDDA.XETRA"))
        print("WELU.XETRA", latest_close("WELU.XETRA"))
        print("GRE.PA", latest_close("GRE.PA"))
