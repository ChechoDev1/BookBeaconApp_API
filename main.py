from flask import Flask
import os
import codigo

app = Flask(__name__)

@app.route('/')
def hello_world():
    try:
        return "Todo gud"
    except Exception as e:
        return "Algo salio mal"

@app.route('/recomendaciones/<uid>')
def recomendaciones(uid):
    return codigo.recomendar_libros(uid)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT', 5000)),debug=False)