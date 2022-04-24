import os
import requests
from dotenv import load_dotenv

load_dotenv()

class GeniusApi:
    '''
        - Classe responsavel pela requisicao com api da Genius 
    '''

    HEADER = {'Authorization': f'{os.getenv("ACCESS_TOKEN")}'}

    def __init__(self, endpoint) -> None:
        if not isinstance(endpoint, str):
            raise Exception('Enpoint must be a string type')
        self.endpoint = endpoint

    def get_artist_informations(self, id: str, sort: str, per_page: int = 10) -> dict:
        if not isinstance(id, str):
            raise Exception('You need pass a string type to get an artist')
        if not isinstance(sort, str):
            raise Exception('Sort must be a string type')
        if not isinstance(per_page, int):
            raise Exception('per_page must be an integer type')

        response = requests.get(f'{self.endpoint}{id}/songs?sort={sort}&per_page={per_page}', headers=self.HEADER)
        return response.json()


if __name__ == '__main__':
    songs = GeniusApi('http://api.genius.com/artists/').get_artist_informations('2300', 'popularity', 10)
    print(songs)