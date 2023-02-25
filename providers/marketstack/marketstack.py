from typing import List, Tuple, Optional

from requests import get
from requests.exceptions import RequestException

TOKEN = "ed61629afad0ad0d882df1ed47f00310"


def latest_close(ticker: List[str]) -> Optional[Tuple[str, float]]:
    if len(ticker) > 0:
        try:
            response = get(f"http://api.marketstack.com/v1/eod?access_key={TOKEN}&symbols={','.join(ticker)}")

            if response.status_code == 200:
                print(response.json())
                return None
            else:
                print(response.status_code)
        except RequestException as e:
            print(e)

            return None
    else:
        return None


if __name__ == "__main__":
    latest_close(["WELU.XETRA", "GRE.XPAR"])
