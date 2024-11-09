# Añadir productos al iniciar la app (en app.py)
productos_collection.insert_many([
    {'nombre': 'Begleri estándar', 'tipo': 'juguetes', 'precio': 200, 'descripcion': 'Begleri medida estandarizanda con contrapesos ligeros hecho a base de paracot', 'imagen_url': 'begleri1.png'},
    {'nombre': 'Begleri imantado', 'tipo': 'juguetes', 'precio': 300, 'descripcion': 'Begleri medida estandarizanda con contrapesos imantados hecho a base de paracot', 'imagen_url': 'begleri2.png'},
    {'nombre': 'Llavero estándar', 'tipo': 'keyrings', 'precio': 100, 'descripcion': 'Llavero hecho a base de paracot trenzado tipo militar para booshcraft', 'imagen_url': 'llavero1.png'},
    {'nombre': 'Pulsera estándar', 'tipo': 'accesorios', 'precio': 250, 'descripcion': 'Pulsera hecha a mano a base de paracot trenzado tipo miltar para booshcraft', 'imagen_url': 'pulsera1.png'}
])