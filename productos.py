from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import certifi

# Configuración de MongoDB
uri = 'mongodb+srv://estradaf809:gmRuDE6tWCmf2B7A@cluster0.8tkxz.mongodb.net/jalawei?retryWrites=true&w=majority'
client = MongoClient(uri, tlsCAFile=certifi.where())

db = client['Asobi']
productos_collection = db['productos']

# Verificar conexión e inicializar productos
def inicializar_productos():
    try:
        client.admin.command('ping')  # Verificar conexión

        # Insertar productos si no existen
        if productos_collection.count_documents({}) == 0:
            productosJ = [
                {"_id": "101", "nombre": "Asobi estándar", "precio": 100, "descripcion": "Begleri medida estandarizada con contrapesos ligeros hecho a base de paracot.", "tipo": "juguete"},
                {"_id": "102", "nombre": "Asobi imantado", "precio": 200, "descripcion": "Begleri medida estandarizada con contrapesos imantados hecho a base de paracot.", "tipo": "juguete"},
            ]
            productos_collection.insert_many(productosJ)
            print("Productos insertados correctamente.")
        else:
            print("Los productos ya existen en la base de datos.")

    except ConnectionFailure:
        print("Error al conectar con MongoDB. Verifica tu conexión a internet y las credenciales.")
    except OperationFailure:
        print("Error en la operación de MongoDB. Verifica los permisos de tu usuario.")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Inicializar productos al importar
inicializar_productos()
