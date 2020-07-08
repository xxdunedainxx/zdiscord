
from zdiscord.service.integration.Integration import IIntegration
import requests
from datetime import datetime

class AlphaV(IIntegration):

    def __init__(self, url: str, token: str):
        super().__init__(name='AlphaV')
        self.url = url # https://www.alphavantage.co
        self.__token = token # ECMHFVPR1RIW8XOQ

    # TODO Get stock by specific date
    def get_stock_info(self, stock: str) -> str:

        dt: datetime.date = datetime.date(datetime.now())
        high: float = 0
        low: float = 0
        avg: float = 0

        try:
            get_time_serie_data: dict = requests.get(f"{self.url}/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={stock}&outputsize=full&apikey={self.__token}").json()["Time Series (Daily)"]

            if get_time_serie_data:
                # TODO Improve this integration
                # Get most recent stocks
                get_time_serie_data=get_time_serie_data[list(get_time_serie_data.keys())[0]]
                print("got stocks..")
                return(f"""--- {stock} STOCK INFO ---\n"""\
                    f"""stock info closed @ {get_time_serie_data['4. close']}\n"""\
                    f"""stock high: {get_time_serie_data['2. high']}\n"""\
                    f"""stock low: {get_time_serie_data['3. low']}\n""" \
                    """--- END STOCK INFO ---""")
            else:
                # TODO Default?
                return f"Failed to get stock info for \'{stock}\'"
        except Exception as e:
            # Logging
            return f"Failed to get stock info for \'{stock}\'"