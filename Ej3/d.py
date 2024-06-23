def option_d(r, geo_key, output_widget):
    output_widget.insert('end', f"El query a correr en cli de redis es: 'ZCARD {geo_key}'\n")
    output_widget.insert('end', f"Dentro de python podemos correr 'r.zcard(geo_key)' siendo geo_key='bataxi', obteniendo \"{r.zcard(geo_key)}\" como respuesta.\n")

