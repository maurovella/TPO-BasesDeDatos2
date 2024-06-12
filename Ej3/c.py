def option_c(r):
    print("El query a correr en cli de redis es: 'KEYS *'")
    print("rta: ", r.keys())