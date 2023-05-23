import requests as rq
import pymongo as pm
import json


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

