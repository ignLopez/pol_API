from flask import Flask, request, abort, jsonify
from flask_restful import Api, Resource, reqparse
import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


app = Flask(__name__)
api = Api(app)

"""
Lee archivo geoJson, retorna un diccionario de instancias de poligonos iterando a travñes de colecciones de coordenadas
"""
def get_polygons():
    geojson = open('map_1.geojson').read()
    data = json.loads(geojson)
    poligonos = {}
    for i in data['features']:
        poligonos[i['properties']['ID']] = Polygon(i['geometry']['coordinates'][0])
    return poligonos

poligonos = get_polygons()

"""
Devuelve el polígono al que pertenece la coordenada
"""
def esta_en_este_poligono(lat,lon):
    coordenadas = Point(lon, lat)
    for j, k in poligonos.items():
        if k.contains(coordenadas):
            return j
    return False


class Item(Resource):
    def post(self):
        if request.json is None:
            return abort(400, "Tienes que pasrme la latitud y longitud mediante un Json")
        else:
            pre_lat = request.json['lat']
            pre_lon = request.json['lon']
            try:
                lat = float(pre_lat)
                lon = float(pre_lon)
                r = esta_en_este_poligono(lat=lat, lon=lon)
                return {'Poligono': r}
            except ValueError:
                return abort(400, "Los datos introducidos no son correctos, no pongas la latitud "
                                  "y longitud con comas ej: 26.42356")

api.add_resource(Item, '/getPol')

if __name__ == '__main__':
    app.run(debug=True)

