import os
import dotenv
import logging
import requests

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_spotify_token():
    configs = {
        'grant_type': 'client_credentials',
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
    }
    url = 'https://accounts.spotify.com/api/token'
    response = requests.post(url, data=configs)
    if response.status_code == 200:
        logger.info('Successfully authenticated')
        return response.json()['access_token']
    else:
        raise Exception(f'failed to get access token: {response.status_code}')


def get_playlist_data(playlist_id, access_token):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            logger.info('Successfully got playlist data')
            return response.json()
        else:
            raise Exception(f'failed to get playlist: {response.status_code}')
    except Exception as e:
        raise Exception(f'failed to get playlist: {e}')


def get_alubum_list(playlist_data):
    names_of_artis = []
    for val in playlist_data.get('tracks')['items']:
        for idx, v in val.items():
            if 'track' in idx:
                tracked_values = val.get('track')
                if 'artists' in tracked_values:
                    artis_data = tracked_values.get('artists')
                    result = [val.get('name') for val in artis_data]
                    names_of_artis.extend(result)
    return names_of_artis


def main():
    try:
        access_token = get_spotify_token()
        playlist_id = '4GJlyc9kdMJOuGfRx3sI8Y'
        playlist_data = get_playlist_data(playlist_id, access_token)
        artists = get_alubum_list(playlist_data)
        print(artists)

    except Exception as e:
        print(f'failed to get playlist: {e}')


if __name__ == '__main__':
    main()

















