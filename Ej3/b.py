
def option_b(r, geo_key):
    # b. ¿Cuantos viajes se generaron a 1 km de distancia de estos 3 lugares?
    text_b ="""
    Los 3 lugares son:
        place: Parque Chas, lon: -58.479258, lat: -34.582497},
        place: UTN, lon: -58.468606, lat: -34.658304},
        place: ITBA Madero, lon: -58.367862, lat: -34.602938}
            """
    print(text_b)
    print("Los queries a correr en el cli de redis son los siguientes: \nGEORADIUS bataxi -58.479258 -34.582497 1 km")
    trips_data_1 = r.georadius(geo_key, -58.479258, -34.582497, 1, 'km', 'WITHDIST', 'WITHCOORD', 'COUNT', 1000)

    print("GEORADIUS bataxi -58.468606 -34.658304 1 km")
    trips_data_2 = r.georadius(geo_key, -58.468606, -34.658304, 1, 'km', 'WITHDIST', 'WITHCOORD', 'COUNT', 1000)

    print("GEORADIUS bataxi -58.367862 -34.602938 1 km")
    trips_data_3 = r.georadius(geo_key, -58.367862, -34.602938, 1, 'km', 'WITHDIST', 'WITHCOORD', 'COUNT', 1000)
