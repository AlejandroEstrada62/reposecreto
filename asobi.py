from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from productos import productos_collection


app = Flask(__name__)
app.secret_key = 'secret_key'

# Modificar la configuración del cliente MongoDB
uri = 'mongodb+srv://estradaf809:gmRuDE6tWCmf2B7A@cluster0.8tkxz.mongodb.net/jalawei?retryWrites=true&w=majority&appName=Cluster0'
try:
    client = MongoClient(uri, 
                        server_api=ServerApi('1'),
                        serverSelectionTimeoutMS=5000)  # Timeout de 5 segundos
    # Verificar la conexión
    client.admin.command('ping')
    print("¡Conexión exitosa a MongoDB!")
    
    db = client['inventario']
    productos_collection = db['productos']
except Exception as e:
    print(f"Error de conexión a MongoDB: {e}")
    exit(1)

@app.route('/')
def index():
    productos = list(productos_collection.find())
    return render_template('index.html', productos=productos)

@app.route('/add_to_cart/<product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    flash('Producto agregado al carrito!', 'success')
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cart_items = []
    if 'cart' in session:
        product_ids = session['cart']
        cart_items = list(productos_collection.find({'_id': {'$in': product_ids}}))
    return render_template('cart.html', cart_items=cart_items)

@app.route('/remove_from_cart/<product_id>')
def remove_from_cart(product_id):
    if 'cart' in session and product_id in session['cart']:
        session['cart'].remove(product_id)
        flash('Producto eliminado del carrito', 'info')
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)