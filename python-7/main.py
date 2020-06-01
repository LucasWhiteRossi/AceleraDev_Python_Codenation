import requests


def get_temperature(lat, lng):
    key = 'e1ee55658d4a2b28c4841e373c3b3d87'
    url = 'https://api.darksky.net/forecast/{}/{},{}'.format(key, lat, lng)
    
    try:
        reponse = requests.get(url)
        data = reponse.json()

        if isinstance(data.get('currently').get('temperature'), (float, int)):
            temperature = data.get('currently').get('temperature')
            return int((temperature - 32) * 5.0 / 9.0)
        else:
            return 'Fail to reach a valid temperature'

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


