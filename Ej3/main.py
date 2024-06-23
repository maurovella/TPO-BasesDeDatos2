import csv
import redis
from tkinter import Tk, Button, Label, filedialog, messagebox, Text, Scrollbar, VERTICAL, RIGHT, Y, END

# Import additional options
# from b import option_b
# from c import option_c
# from d import option_d
# from e import option_e

def connect_to_redis():
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        return r
    except redis.ConnectionError:
        messagebox.showerror("Connection Error", "Unable to connect to Redis server.")
        return None

def import_csv_to_redis():
    file_path = 'Ej3/bataxi.csv'
    r = connect_to_redis()
    if r is None:
        return

    geo_key = 'bataxi'
    try:
        with open(file_path, mode='r', encoding='utf-8-sig') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                id = row['id_viaje_r']
                longitude = float(row['origen_viaje_x'])
                latitude = float(row['origen_viaje_y'])
                r.geoadd(geo_key, (longitude, latitude, id))
        messagebox.showinfo("Success", "Geospatial data added to Redis.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

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

def option_c(r, output_widget):
    output_widget.insert('end', "El query a correr en cli de redis es: 'KEYS *'\n")
    output_widget.insert('end', f"Dentro de python podemos correr 'len(r.keys())', obteniendo \"{len(r.keys())}\" como respuesta.\n")

def option_d(r, geo_key, output_widget):
    output_widget.insert('end', f"El query a correr en cli de redis es: 'ZCARD {geo_key}'\n")
    output_widget.insert('end', f"Dentro de python podemos correr 'r.zcard(geo_key)' siendo geo_key='bataxi', obteniendo \"{r.zcard(geo_key)}\" como respuesta.\n")

def option_e(output_widget):
    output_widget.insert('end', "Se utiliza un sorted set con una tecnica llamada geo hash, donde los bits de latitud y longitud se entrelazan para formar un entero unico de 52bits\n")


def handle_option_b(output_widget):
    r = connect_to_redis()
    if r is not None:
        option_b(r, 'bataxi', output_widget)

def handle_option_c(output_widget):
    r = connect_to_redis()
    if r is not None:
        option_c(r, output_widget)

def handle_option_d(output_widget):
    r = connect_to_redis()
    if r is not None:
        option_d(r, 'bataxi', output_widget)

def handle_option_e(output_widget):
    option_e(output_widget)

def create_gui():
    window = Tk()
    window.title("Redis Geospatial Data")
    import_csv_to_redis()

    Label(window, text="Elija una opción:").pack()

    output_widget = Text(window, wrap='word')
    output_widget.pack(expand=True, fill='both')

    scrollbar = Scrollbar(window, orient=VERTICAL, command=output_widget.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    output_widget.config(yscrollcommand=scrollbar.set)

    Button(window, text="¿Cuantos viajes se generaron a 1km de distacia de los 3 lugares mencionados?", command=lambda: handle_option_b(output_widget)).pack()
    Button(window, text="¿Cuantas KEYS hay en la base de datos Redis?", command= lambda: handle_option_c(output_widget)).pack()
    Button(window, text="¿Cuantos miembros tiene la key 'bataxi'?", command=lambda: handle_option_d(output_widget)).pack()
    Button(window, text="¿Sobre qué estructura de Redis trabaja el GeoADD", command=lambda: handle_option_e(output_widget)).pack()

    window.mainloop()

if __name__ == "__main__":
    create_gui()
