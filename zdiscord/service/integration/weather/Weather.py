from zdiscord.service.integration.Integration import IIntegration
import requests

class Weather(IIntegration):

    def __init__(self, url: str, token: str):
        super().__init__(name='Weather')
        self.url = url
        self.__token = token

    def get_and_format(self, query: str) -> str:
        weather_info: requests.Response = self.get_weather(query)

        if (weather_info.status_code != 200):
            "there is no weather today :( \n (something went wrong)\nNOTE: You must submit your query something like: \'Town,State\'"
        else:
            return self.format_weather(weather_info.json())

    def format_weather(self, weatherResponse: {}) -> str:
        weather_description: str = ''

        for weather_descriptions in weatherResponse['weather']:
            weather_description += weather_descriptions['description']

        return f"""Description: {weather_description}
    Wind Speed: {str(weatherResponse['wind']['speed'])} mph
    Temperature: {str(weatherResponse['main']['temp'])} °F
    Humans say the temperature feels like.. {str(weatherResponse['main']['feels_like'])} °F"""

    def get_weather(self, query: str) -> requests.Response:
        url = f"{self.url}/weather?q={query}&APPID={self.__token}&units=imperial"
        return requests.get(url)
