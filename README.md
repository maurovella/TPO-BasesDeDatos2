# TPO-BasesDeDatos2
## Trabajo Práctico Obligatorio Base de Datos II ITBA 2C2024

<u>Integrantes:</u> \
Altman Sofía, Paula \
Luchetti, Matías \
Vella, Mauro

<u>Grupo: 11</u>

• Fecha de entrega: 19 de junio de 2024 \
• Forma de entrega: a través de Codespace en Github. Adicionalmente realizar un
informe/presentación para su defensa, donde se muestren los comandos utilizados
para resolver cada punto \
• Repositorio de datasets: https://l1nk.dev/aTrRE 

A fines de presentacion, se incluyo todo el procedimiento y resultados obtenidos en este README mientras que cada carpeta tiene los codigos especificos a la resolucion de cada ejercicio

<br/>
<br/>


# Respuestas al Enunciado

## 1. MongoDB
### 1.a
Se importa albumlist.csv a un coleccion:
```bash	
mongoimport --host localhost --db mymongo --collection Album --type csv --file albumlist.csv --headerline
```

### 1.b
Se cuenta la cantidad de álbumes por año y ordénelos de manera descendente
```javascript
db.getCollection('Album').aggregate(
  [
    {
      $group: {
        _id: '$Year',
        totalAlbums: { $sum: 1 }
      }
    },
    { $sort: { totalAlbums: -1 } }
  ]);
```
### 1.c y 1.d
Se le agrega un nuevo atributo llamado `score` que sea `501-Number`, y muestre el valor de 'score' para cada artista.

```javascript
db.getCollection('Album').aggregate(
  [
    {
      $addFields: {
        score: { $subtract: [501, '$Number'] }
      }
    },
    {
      $group: {
        _id: '$Artist',
        scores: { $sum: '$score' }
      }
    }
  ]);
```


## 2. Neo4j
### Primero, abrir un sandbox en https://sandbox.neo4j.com/
### Para setear el ambiente
```javascript
LOAD CSV WITH HEADERS FROM "https://data.neo4j.com/northwind/products.csv" AS row
CREATE (n:Product)
SET n = row,
n.unitPrice = toFloat(row.unitPrice),
n.unitsInStock = toInteger(row.unitsInStock), n.unitsOnOrder = toInteger(row.unitsOnOrder),
n.reorderLevel = toInteger(row.reorderLevel), n.discontinued = (row.discontinued <> "0")


LOAD CSV WITH HEADERS FROM "https://data.neo4j.com/northwind/categories.csv" AS row
CREATE (n:Category)
SET n = row

LOAD CSV WITH HEADERS FROM "https://data.neo4j.com/northwind/suppliers.csv" AS row
CREATE (n:Supplier)
SET n = row

MATCH (p:Product),(c:Category)
WHERE p.categoryID = c.categoryID
CREATE (p)-[:PART_OF]->(c)

MATCH (p:Product),(s:Supplier)
WHERE p.supplierID = s.supplierID
CREATE (s)-[:SUPPLIES]->(p)
```

### 2.a
Para mostrar cuantos productos hay en la base:
```javascript
MATCH(p:Product) RETURN COUNT(p) AS TotalProducts
```
El resultado es: 
```javascript
TotalProducts : 77
```

### 2.b
Para mostrar cuanto cuesta el `Queso Cabrales`:
``` javascript
MATCH(p:Product) WHERE p.productName = 'Queso Cabrales' RETURN p.productName, p.unitPrice
```

El resultado es: 
``` javascript
p.productName : 'Queso Cabrales' , p.unitPrice : '21.0' 
```

### 2.c
Para mostrar cuantos productos pertenecen a la categoría `Condiments`:
``` javascript
MATCH(p:Product) --( c:Category) WHERE p.categoryID= c.categoryID AND c.categoryName = 'Condiments' RETURN Count(p) as TotalCondiments
```

El resultado es:
``` javascript
TotalCondiments : 12
```

### 2.d
Para mostrar  cuál es el nombre y el precio unitario de los tres productos más caros del conjunto de productos que ofrecen los proveedores de `UK`
``` javascript
MATCH(p:Product)--(s:Supplier) WHERE p.supplierID = s.supplierID AND s.country = 'UK' return p.productName, p.unitPrice LIMIT 3
```
El resultado es:
``` javascript
p.productName	p.unitPrice
"Chang"	19.0
"Chai"	18.0
"Aniseed Syrup"	10.0
```

## 3. Redis

### Prerequisitos
```bash
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

sudo apt-get update
sudo apt-get install redis

sudo service redis-server start

redis-cli
```
### 3.a
Paso 1: se importan csv y redis en python
```python
import csv
import redis
```
Paso 2: se crea la conexión con la base de datos y creamos una variable con la clave
```python
r = redis.Redis(host='localhost', port=6379, db=0)
geo_key = 'bataxi'
```

Paso 3: se lee el archivo csv y se insertan los datos en la base de datos
```python
with open('path/to/bataxi.csv', mode='r', encoding='utf-8-sig') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        id = row['id_viaje_r']
        longitude = row['origen_viaje_x']
        latitude = row['origen_viaje_y']
        r.geoadd(geo_key, (longitude, latitude, id))
```

### 3.b
Los 3 lugares son:
```javascript
places = [  {"place":"Parque Chas", "lon": -58.479258, "lat": -34.582497},
            {"place":"UTN" , "lon": -58.468606, "lat": -34.658304},
            {"place":"ITBA Madero", "lon": -58.367862, "lat": -34.602938}
        ];
```

Los queries a correr en el cli de redis para obtener los resultados son:
```bash 
GEORADIUS bataxi -58.479258 -34.582497 1 km
GEORADIUS bataxi -58.468606 -34.658304 1 km
GEORADIUS bataxi -58.367862 -34.602938 1 km
```

GEORADIUS es un comando de redis que dado el dataset (bataxi), y en este caso las cordenadas y la distancia, devuelve los puntos que se encuentran a esa distancia o menos de las coordenadas dadas.

Como resultado se obtienen: `339` `9` `242` respectivamente.

### 3.c
Para obtener la cantidad de KEYS que hay en la base de datos de Redis:
```bash
KEYS *
```

KEYS es un comando de redis que devuelve todas las keys que hay en la base de datos que coincidan con el patrón dado.

Como resultado se obtiene `1` que es la cantidad de keys que hay en la base de datos de Redis.

### 3.d
Para obtener la cantidad de miembros que tiene la key 'bataxi' se corre el siguiente comando en el cli:

```bash
ZCARD bataxi
```

ZCARD es un comando de redis que devuelve la cardinalidad (cantidad de elementos) del sorted set almacenado en la clave dada.
Como el resultado se obtiene: 19148

### 3.e
Se utiliza un sorted set con una técnica llamada Geohash, donde los bits de latitud y longitud se entrelazan para formar un entero único de 52 bits.