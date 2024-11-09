# app.py
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

import config
app = Flask(__name__)

# Conectar a MongoDB
client = MongoClient(config.MONGO_URI)
db = client['Asobi']  # Nombre de tu base de datos
productos_collection = db['productos']  # Colección para productos

# Añadir productos al iniciar la app (en app.py)
productos_collection.insert_many([
    {'nombre': 'Begleri estándar', 'tipo': 'juguetes', 'precio': 200, 'descripcion': 'Begleri medida estandarizanda con contrapesos ligeros hecho a base de paracot', 'imagen_url': 'begleri1.png'},
    {'nombre': 'Begleri imantado', 'tipo': 'juguetes', 'precio': 300, 'descripcion': 'Begleri medida estandarizanda con contrapesos imantados hecho a base de paracot', 'imagen_url': 'begleri2.png'},
    {'nombre': 'Llavero estándar', 'tipo': 'keyrings', 'precio': 100, 'descripcion': 'Llavero hecho a base de paracot trenzado tipo militar para booshcraft', 'imagen_url': 'llavero1.png'},
    {'nombre': 'Pulsera estándar', 'tipo': 'accesorios', 'precio': 250, 'descripcion': 'Pulsera hecha a mano a base de paracot trenzado tipo miltar para booshcraft', 'imagen_url': 'pulsera1.png'}
])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/productos/<tipo>')
def productos(tipo):
    # Obtener productos de un tipo específico desde MongoDB
    productos = productos_collection.find({'tipo': tipo})
    return render_template('productos.html', productos=productos)

@app.route('/producto/<producto_id>')
def producto(producto_id):
    # Obtener un producto específico
    producto = productos_collection.find_one({'_id': producto_id})
    return render_template('producto.html', producto=producto)

@app.route('/carrito')
def carrito():
    return render_template('carrito.html')

@app.route('/compra')
def compra():
    return render_template('compra.html')

if __name__ == '__main__':
    app.run(debug=True)

