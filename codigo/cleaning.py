import requests as rq
import pymongo as pm
import json


#Generamos la conexion mediante un client nuevo
client=pm.MongoClient("localhost", 27017)

#Creamos una nueva db
db=client.ghibli
#Generamos la nueva coleccion
movies=db.movies

#Quitar el campo anidado "still" pues solo habia un documento que lo tenia lleno
db.movies.update_many({}, { '$unset': { "character.$[].still": 1 } })

#Cambiar el arreglo vacio en el campo "awards" de aquellas peliculas que no tienen premios
db.movies.update_many({ 'awards': [''] }, { '$set': { 'awards': 'None' } })

#Modificar el titulo original (hepburn) que estaba mal escrito en la API
db.movies.update_one({'title':'Whisper of the Heart'}, {'$set':{'hepburn':'Mimi o Sumaseba'}})

# Cambiar el tipo de dato de budgetUSD y de boxOfficeUSD de string a int
##En lugar de 'Unkown', 'N/A' y 'TBA', ponerles '0' para poder convertir
db.movies.update_many({'budgetUSD':{'$eq':'Unknown'}}, {'$set':{'budgetUSD':'0'}})
db.movies.update_many({'budgetUSD':{'$eq':'N/A'}}, {'$set':{'budgetUSD':'0'}})
db.movies.update_many({'budgetUSD':{'$eq':'TBA'}}, {'$set':{'budgetUSD':'0'}})

##Quitarle las comas
db.movies.update_many({}, [{'$addFields':{'budgetUSD':{'$replaceAll':{'input':'$budgetUSD', 'find':',', 'replacement':''}}}}])

##Convertir a double
db.movies.update_many( {}, [{ '$set': { 'budgetUSD': { '$toDouble': '$budgetUSD' } } }])

##Imputar con criterio de media aquellos valores que tienen 0
###Obtener la media
budgetMean = list(db.movies.aggregate([{'$match':  {'budgetUSD':{'$ne': 0 }}},{ '$group': {'_id': None, 'averageBudget': { '$avg': "$budgetUSD" }}}]))

###Imputacion
db.movies.update_many({'budgetUSD':0}, {'$set':{'budgetUSD':budgetMean[0]['averageBudget']}})

##Repetir para boxOfficeUSD pero solo existen 'Unknown" y 'TBD'
db.movies.update_many({'boxOfficeUSD':{'$eq':'Unknown'}}, {'$set':{'boxOfficeUSD':'0'}})
db.movies.update_many({'boxOfficeUSD':{'$eq':'TBD'}}, {'$set':{'boxOfficeUSD':'0'}})
db.movies.update_many({}, [{'$addFields':{'boxOfficeUSD':{'$replaceAll':{'input':'$boxOfficeUSD', 'find':',', 'replacement':''}}}}])
db.movies.update_many( {}, [{ '$set': { 'boxOfficeUSD': { '$toDouble': '$boxOfficeUSD' } } }])
boxOfficeMean = list(db.movies.aggregate([{'$match':  {'boxOfficeUSD':{'$ne': 0 }}},{ '$group': {'_id': None, 'averageBboxOffice': { '$avg': "$boxOfficeUSD" }}}]))
db.movies.update_many({'boxOfficeUSD':0}, {'$set':{'boxOfficeUSD':boxOfficeMean[0]['averageBboxOffice']}})


#Cambiar el tipo de dato de runtimeMinutes
##Imputamos por 0 las que tienen 'TBA'
db.movies.update_many({'runtimeMinutes':{'$eq':'TBA'}}, {'$set':{'runtimeMinutes':'0'}})

##Convertimos
db.movies.update_many( {}, [{ '$set': { 'runtimeMinutes': { '$toInt': '$runtimeMinutes' } } }])

#Imputar los atributos anidados de character vacios
db.movies.update_many({'character': { '$all': [{ "$elemMatch" : { 'name': "", 'originalCast': "", 'lastEnglishDubbingActor': "" } }] }}, { '$set': { "character.$[].name": 'TBA', "character.$[].originalCast": 'TBA', "character.$[].lastEnglishDubbingActor": 'TBA'  } })
