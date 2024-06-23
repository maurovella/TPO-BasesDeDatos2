def option_c(r):
    print("El query a correr en cli de redis es: 'KEYS *'")
    print(f"Dentro de python podemos correr 'len(r.keys())', obteniendo \"{len(r.keys())}\" como respuesta.")
