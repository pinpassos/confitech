import uuid
import boto3
import json
from flask import Flask, render_template
from redis import Redis
from api.GeniusApi import GeniusApi 
from flask_restful import Resource, Api

# instâncas do flask e flask-restful
app = Flask(__name__)
api = Api(app)

# redis connection
redis = Redis(host='localhost', port='6379')
# informa que os dados devem expirar em sete dias
redis.expire(redis.flushall(), 604800)

# boto3 - DynamoDB
dynamodb = boto3.resource('dynamodb')
dynamo_table = dynamodb.Table('Artist')


class Artist(Resource):
    def get(self, artist_id: str) -> dict:

        # verifica se existe transacao no cache, se nao existir consulta da api genius e salva no redis
        if redis.exists(artist_id) == 0:
            artist = GeniusApi('http://api.genius.com/artists/').get_artist_informations(artist_id, 'popularity', 10)
            artist_dict = {
                'artist_id': artist_id, 
                'artist_name': artist.get('response').get('songs')[0].get('primary_artist').get('name'),
                'artist_top_songs': [song['title'] for song in artist.get('response').get('songs')]
                }
            # Salva os dados de id no formato uuid4, nome do artista e uma lista com as dez músicas mais populares no DynamoDB
            dynamo_table.put_item(
                Item = {
                    'artist_id': str(uuid.uuid4()),
                    'artist_name': artist.get('response').get('songs')[0].get('primary_artist').get('name'),
                    'artist_top_songs': [song['title'] for song in artist.get('response').get('songs')]
                    }
                )
            # Salva dados no redis
            redis.set(artist_id, json.dumps(artist_dict))
            # retorna dados da api da genius para a API
            return artist_dict

        # caso consulta esteja salva no redis retorna os dados em cache para a API
        elif redis.exists(artist_id) == 1:
            # retorna dados do redis para a API
            artist_from_redis = redis.get(artist_id)
            return json.loads(artist_from_redis)

# Endpoint principal da nossa api
# Exemplo de consulta: http://127.0.0.1:5000/16775/
api.add_resource(Artist, '/<string:artist_id>/')

if __name__ == '__main__':
    app.run(debug=True)