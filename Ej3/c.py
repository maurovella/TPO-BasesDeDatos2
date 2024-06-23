def option_c(r, output_widget):
    output_widget.insert('end', "El query a correr en cli de redis es: 'KEYS *'\n")
    output_widget.insert('end', f"Dentro de python podemos correr 'len(r.keys())', obteniendo \"{len(r.keys())}\" como respuesta.\n")