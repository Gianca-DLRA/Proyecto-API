# Proyecto-API
Repositorio del proyecto de BDNR con la API de Studio Ghibli

## Descripción
- environment.yml: Script para crear el conda environment *ghibliAPI* 
### codigo
En esta carpeta se encuentran los scripts de *python*, el archivo de texto *movies.txt* con la lista de pelis, 2 archivos .JSON por 2 peliculas que no cargaban bien desde la API.
### Docker
Encontramos el docker-compose que construye los contenedores de *neo4j* y de *mongo*, al igual que el archivo de instrucciones para la conexion a neo4j desde mongo. 
### Queries
Encontramos las *queries* tanto de *mongosh* como de *cypher*

## Conexion de API a MongoDB
Script: *ghibli.py* 
### Instrucciones
1. Crear el conda environment con 
```sh
conda create -f environment.yml
```
2. Una vez activado el environment, navegar a la carpeta *Docker*, donde esta el docker-compose y correr:
```sh
docker-compose up
```
o bien, 
```sh
docker compose up
```
Esto levanta los contenedores.
3. Ya con el conda activado y el docker levantado, seguir las instrucciones de */Docker/instructivo.txt*:
a) Asegurate que el docker compose este levantado
b) A traves de linea de comando, accede al folder pulgins
c) Corre los siguientes comandos:
```sh
   sudo wget https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/5.6.0/apoc-mongodb-dependencies-5.6.0-all.jar
   sudo wget https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/5.6.0/apoc-5.6.0-extended.jar
```
 d) Reinicia el docker
 Estos pasos dejan lista la conexion de *neo4j* y *mongo*.
4. Correr el script *ghibli.py*. Si es en terminal, asegurate de tener activado el environment:
```sh
python3 ghibli.py
```

## ETL de la base de datos
### Instrucciones
Este paso se hizo directo desde mongodb. Para ello:
1. Correr *cleaning.py*
```sh
python3 cleaning.py
```

## Conexion a *neo4j*
Para la conexion consideramos las relaciones entre las peliculas, sus personajes y sus ratings.
### Instrucciones
1. Correr *Load.py*
```sh
python3 Load.py
```


