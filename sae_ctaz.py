import json
import pycurl
from io import BytesIO


def sae_to_geojson():
    """
    Transforms http://api.consorciozaragoza.es/api/1/sae JSON data to GeoJSON
    """
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://api.consorciozaragoza.es/api/1/sae')
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    response_code = c.getinfo(pycurl.RESPONSE_CODE)
    c.close()

    # Creates GeoJSON with no features
    return_json = {
        'type': 'FeatureCollection',
        'features': []
        }

    if response_code == 200:  # OK
        body = buffer.getvalue()
        sae_json = json.loads(body.decode('utf-8'))

        # For every bus in sae_json, transform it to a point feature and append it to the GeoJSON
        for i in sae_json['sae']:
            point = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [float(i['longitud']), float(i['latitud'])]
                },
                'properties': {
                    'busNumber': i['bus'],
                    'lineNumber': i['linea'],
                    'lineName': i['nombre_linea'],
                    'lastUpdated': i['momento']
                }
            }
            return_json['features'].append(point)

        return return_json

    else:
        # Something went wrong
        print("Error", response_code)
        return return_json


if __name__ == "__main__":
    print(json.dumps(sae_to_geojson()))
