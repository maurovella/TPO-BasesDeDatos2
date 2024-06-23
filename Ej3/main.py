import csv 
import redis
from b import option_b
from c import option_c
from d import option_d
from e import option_e


r = redis.Redis(host='localhost', port=6379, db=0)
geo_key = 'bataxi'

print("Adding data to redis...")

# a. Importar los datos del archivo a Redis
with open('Ej3/bataxi.csv', mode='r', encoding='utf-8-sig') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        id = row['id_viaje_r']
        longitude = row['origen_viaje_x']
        latitude = row['origen_viaje_y']
        r.geoadd(geo_key, (longitude, latitude, id))

print("Geospatial data added to Redis.\n")

# Print menu with 4 query options
text = """
Elija una opción entre las consignas:
b: ¿Cuantos viajes se generaron a 1 km de distancia de los 3 lugares mencionados?
c: ¿Cuántas KEYS hay en la base de datos Redis?
d: ¿Cuántos miembros tiene la key 'bataxi'?
e: ¿Sobre qué estructura de Redis trabaja el GeoADD?
"""

option = input(text)

if option == 'b':
    option_b(r, geo_key)
if option == 'c':
    option_c(r)
if option == 'd':
    option_d(r, geo_key)
if option == 'e':
    option_e()
