from zdiscord.service.integration.Integration import IIntegration
from zdiscord.util.general.world.UsaConversionTables import UsaConversionTables
import requests

class Weather(IIntegration):

    def __init__(self, url: str, token: str):
        super().__init__(name='Weather')
        self.url = url
        self.__token = token

    def get_and_format(self, query: str) -> str:
        weather_info: requests.Response = self.get_weather(query)

        if (weather_info.status_code != 200):
            try:
                query_split=query.split(',')
                query=f"{query_split[0]},{UsaConversionTables.abbrev_us_state[query_split[1]]}"
                weather_info: requests.Response = self.get_weather(query)
                if (weather_info.status_code != 200):
                    return "there is no weather today :( \n (something went wrong)\nNOTE: You must submit your query something like: \'Town,State\'"
                else:
                    return self.format_weather(weather_info.json())
            except Exception as e:
                return "there is no weather today :( \n (something went wrong)\nNOTE: You must submit your query something like: \'Town,State\'"
        else:
            return self.format_weather(weather_info.json())

    def format_weather(self, weatherResponse: {}) -> str:
        weather_description: str = ''

        for weather_descriptions in weatherResponse['weather']:
            weather_description += weather_descriptions['description']

        return (f"""Description: {weather_description}\n"""\
                f"""Wind Speed: {str(weatherResponse['wind']['speed'])} mph\n"""\
                f"""Temperature: {str(weatherResponse['main']['temp'])} °F\n"""\
                f"""Humans say the temperature feels like.. {str(weatherResponse['main']['feels_like'])} °F"""
        )

    def get_weather(self, query: str) -> requests.Response:
        url = f"{self.url}/weather?q={query}&APPID={self.__token}&units=imperial"
        return requests.get(url)
