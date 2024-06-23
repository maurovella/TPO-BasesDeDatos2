def option_d(r, geo_key):
    print(f"El query a correr en cli de redis es: 'ZCARD {geo_key}'")
    print(f"Dentro de python podemos correr 'r.zcard(geo_key)' siendo geo_key='bataxi', obteniendo \"{r.zcard(geo_key)}\" como respuesta.")

