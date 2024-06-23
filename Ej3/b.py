def option_b(r, geo_key, output_widget):
    # b. ¿Cuantos viajes se generaron a 1 km de distancia de estos 3 lugares?
    text_b ="""
    Los 3 lugares son:
        place: Parque Chas, lon: -58.479258, lat: -34.582497
        place: UTN, lon: -58.468606, lat: -34.658304
        place: ITBA Madero, lon: -58.367862, lat: -34.602938
    """
    output_widget.insert('end', text_b + "\n")
    output_widget.insert('end', "Los queries a correr en el cli de redis son los siguientes: \nGEORADIUS bataxi -58.479258 -34.582497 1 km\n")
    trips_data_1 = r.georadius(geo_key, -58.479258, -34.582497, 1, 'km', 'WITHDIST', 'WITHCOORD', 'COUNT', 1000)

    output_widget.insert('end', "GEORADIUS bataxi -58.468606 -34.658304 1 km\n")
    trips_data_2 = r.georadius(geo_key, -58.468606, -34.658304, 1, 'km', 'WITHDIST', 'WITHCOORD', 'COUNT', 1000)

    output_widget.insert('end', "GEORADIUS bataxi -58.367862 -34.602938 1 km\n")
    trips_data_3 = r.georadius(geo_key, -58.367862, -34.602938, 1, 'km', 'WITHDIST', 'WITHCOORD', 'COUNT', 1000)

    output_widget.insert('end', "En python podemos correr 'len(r.georadius(geo_key, longitud, latitud, radio, 'unidad_de_medida', 'WITHDIST', 'WITHCOORD', 'COUNT', 1000))' para obtener la cantidad de viajes generados\n")

    # print trips_data count
    output_widget.insert('end', f"La cantidad de viajes generados a 1 km de Parque Chas es: {len(trips_data_1)}\n")
    output_widget.insert('end', f"La cantidad de viajes generados a 1 km de UTN es: {len(trips_data_2)}\n")
    output_widget.insert('end', f"La cantidad de viajes generados a 1 km de ITBA Madero es: {len(trips_data_3)}\n")
