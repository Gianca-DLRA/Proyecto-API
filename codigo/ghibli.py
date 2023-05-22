import requests as rq
import pymongo as pm
import json
from neo4j import GraphDatabase

#Creamos uns clase de coneccion para conectarse a la base de datos de grafos
class Neo4jConnection:
    
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def query(self, query, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response

#Generamos la conexion mediante un client nuevo
client=pm.MongoClient("localhost", 27017)

#Creamos una nueva db
db=client.ghibli
#Generamos la nueva coleccion
movies=db.movies

#Obtenemos las peliculas de un .txt y las guardamos en una lista
movies_list=[]
with open("movies.txt", "r") as f:
    for movie in f:
        movies_list.append(movie.strip("\n"))

print(movies_list)

#Obtenemos las peliculas
for movie in movies_list:
    r=rq.get("https://studio-ghibli-films-api.herokuapp.com/api/"+movie)
    if r.status_code==200:
        response=r.json()
        print(movie)
        movies.insert_one(response)    #Insertamos en la coleccion movies
    else:
        print("Pelicula no encontrada\n")

#Agregamos las dos peliculas que faltan porque el JSON desde la API no se convertian bien
with open("hdyl.json", "r") as f:
    hdyl=json.load(f)
    movies.insert_one(hdyl)
print("How Do You Live?")

with open("kaguya.json", "r") as f:
    kaguya=json.load(f)
    movies.insert_one(kaguya)
print("The Tale of the Princess Kaguya")


### LLENAR DATOS FALTANTES

#Creamos la conexion con neo4j (Cambiar passwords etc)
conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="7734")


#Se crea el texto de la query para convertir los documentos JSON en grafos 
### INCLUIR CORREGIR HOST
docAGraf = "CALL apoc.mongodb.get('mongodb://mongo:neo4j@mongo:27017', 'ghibli', 'movies', {}, true) YIELD value CALL apoc.graph.fromDocument(value, {write: true, mappings: {`$`: 'Ghibli{*, @reviews}',`$.character`: 'Character{!name,originalCast,lastEnglishDubbingActor}'}}) YIELD graph AS g1 return g1"

conn.query(docAGraf)

