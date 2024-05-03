from flask import Flask
import os
import codigo
from codigo import db, recomendar_libros

app = Flask(__name__)

@app.route('/')
def hello_world():
    try:
        return "Todo gud"
    except Exception as e:
        return "Algo salio mal"

@app.route('/recomendaciones/<uid>')
def recomendaciones(uid):
    # Obtener los géneros y autores favoritos del usuario desde Firestore
    datos_usuario = db.collection('users').document(uid).get().to_dict()
    generos_favoritos = datos_usuario.get('genres', [])
    autores_favoritos = datos_usuario.get('authors', [])
    
    # Llamar a la función recomendar_libros con los géneros y autores favoritos
    libros_recomendados = codigo.recomendar_libros(generos_favoritos, autores_favoritos)
    
    return libros_recomendados.to_json()  # Devolver los resultados como JSON

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT', 5000)),debug=False)