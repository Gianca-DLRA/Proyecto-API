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

#Creamos la conexion con neo4j (Cambiar passwords etc)
conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="7734")


#Se crea el texto de la query para convertir los documentos JSON en grafos 
### INCLUIR CORREGIR HOST
docAGraf = "CALL apoc.mongodb.get('mongodb://mongo:neo4j@mongo:27017', 'ghibli', 'movies', {}, true) YIELD value CALL apoc.graph.fromDocument(value, {write: true, mappings: {`$`: 'Ghibli{*, @reviews}',`$.character`: 'Character{!name,originalCast,lastEnglishDubbingActor}'}}) YIELD graph AS g1 return g1"

#Se realiza la carga
conn.query(docAGraf)

#Cerramos la conexion
conn.close()