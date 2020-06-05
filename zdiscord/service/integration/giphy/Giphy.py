from zdiscord.service.integration.Integration import IIntegration
import requests

class Giphy(IIntegration):

    def __init__(self, url: str, token: str, default_giphy: str = 'https://giphy.com/embed/8F32Q0H0L8zyTSCCYI'):
        super().__init__(name='Giphy')
        self.url = url
        self.__token = token
        self.default_giphy = default_giphy

    def get_giphy(self, query: str):
        r = requests.get(f"{self.url}/search?api_key={self.__token}&q={query}&limit=1&offset=0&rating=G&lang=en")
        if r.status_code == 200:
            return r.json()['data'][0]['embed_url']
        else:
            return self.default_giphy
