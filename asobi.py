# app.py
from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from bson import ObjectId
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# Conectar a MongoDB
client = MongoClient(config.MONGO_URI)
db = client['Asobi']
productos_collection = db['productos']

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
    try:
        # Imprimir para debug
        print(f"Buscando producto con ID: {producto_id}")
        
        producto = productos_collection.find_one({'_id': ObjectId(producto_id)})
        
        # Imprimir para debug
        print(f"Producto encontrado: {producto}")
        
        if producto:
            return render_template('producto.html', producto=producto)
        return "Producto no encontrado", 404
    except Exception as e:
        print(f"Error detallado: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return "Error al cargar el producto", 500

@app.route('/carrito', methods=['GET'])
def carrito():
    try:
        # Obtener el carrito de la sesión o una lista vacía si no existe
        carrito_items = session.get('carrito', [])
        
        # Imprimir para debug
        print("Items en el carrito:", carrito_items)
        
        # Calcular el total solo si hay items
        total = sum(float(item.get('subtotal', 0)) for item in carrito_items) if carrito_items else 0
        
        return render_template('carrito.html', items=carrito_items, total=total)
    except Exception as e:
        print(f"Error en carrito: {str(e)}")
        # Si hay un error, inicializar un carrito vacío
        session['carrito'] = []
        return render_template('carrito.html', items=[], total=0)

@app.route('/compra')
def compra():
    return render_template('compra.html')

@app.route('/agregar-al-carrito', methods=['POST'])
def agregar_al_carrito():
    try:
        producto_id = request.form.get('producto_id')
        cantidad = int(request.form.get('cantidad', 1))
        
        # Imprimir para debug
        print(f"Producto ID recibido: {producto_id}")
        
        # Buscar el producto en la base de datos
        producto = productos_collection.find_one({'_id': ObjectId(producto_id)})
        
        if producto:
            # Asegurarse de que el carrito existe en la sesión
            if 'carrito' not in session:
                session['carrito'] = []
            
            # Crear item del carrito con la información necesaria
            item_carrito = {
                'id': str(producto['_id']),
                'nombre': str(producto['nombre']),
                'precio': float(producto['precio']),
                'cantidad': int(cantidad),
                'imagen_url': str(producto['imagen_url']),
                'tipo': str(producto['tipo']),
                'subtotal': float(producto['precio']) * int(cantidad)
            }
            
            # Imprimir para debug
            print(f"Item carrito creado: {item_carrito}")
            
            # Agregar el item al carrito
            carrito = session.get('carrito', [])
            carrito.append(item_carrito)
            session['carrito'] = carrito
            session.modified = True
            
            return redirect(url_for('carrito'))
        
        return "Producto no encontrado", 404
    except Exception as e:
        print(f"Error al agregar al carrito: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return f"Error al agregar al carrito: {str(e)}", 400

@app.route('/eliminar-del-carrito/<int:index>', methods=['POST'])
def eliminar_del_carrito(index):
    try:
        if 'carrito' in session:
            carrito = session['carrito']
            if 0 <= index < len(carrito):
                carrito.pop(index)
                session['carrito'] = carrito
                session.modified = True
        return redirect(url_for('carrito'))
    except Exception as e:
        print(f"Error al eliminar del carrito: {str(e)}")
        return redirect(url_for('carrito'))

if __name__ == '__main__':
    app.run(debug=True)

