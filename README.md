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

 


