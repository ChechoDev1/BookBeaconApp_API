import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from firebase_admin import credentials, firestore, initialize_app

# Inicializar la app de Firebase
cred = credentials.Certificate("key.json")
initialize_app(cred)
db = firestore.client()

# Vectorización
vectorizer = TfidfVectorizer()

# Modelo de vecinos más cercanos
model_knn = NearestNeighbors(metric='cosine', algorithm='brute')

def cargar_datos_usuarios():
    usuarios = db.collection('users').stream()
    datos_usuarios = []
    for usuario in usuarios:
        datos_usuario = usuario.to_dict()
        datos_usuarios.append(datos_usuario)
    return pd.DataFrame(datos_usuarios)

def cargar_datos_libros_desde_csv(ruta):
    return pd.read_csv(ruta)

def recomendar_libros(generos_favoritos, autores_favoritos):
    # Cargar los datos de los usuarios desde Firestore
    df_usuarios = cargar_datos_usuarios()
    
    # Cargar los datos de los libros desde un archivo CSV
    df_libros = cargar_datos_libros_desde_csv('Goodreads_books_with_genres_simplificado.csv')
    df_libros = df_libros[df_libros['num_pages'] != 0]
    df_libros = df_libros.dropna()
    
    # Combinar géneros y autores en una sola columna
    df_libros['text'] = df_libros['genres'] + ';' + df_libros['Author']
    
    # Vectorización
    tfidf_matrix = vectorizer.fit_transform(df_libros['text'])
    
    # Entrenar el modelo de vecinos más cercanos
    model_knn.fit(tfidf_matrix)
    
    # Crear el texto de entrada del usuario
    texto_usuario = ';'.join(generos_favoritos + autores_favoritos)
    
    # Convertir el texto del usuario en un vector TF-IDF
    vector_usuario = vectorizer.transform([texto_usuario])
    
    # Encontrar los vecinos más cercanos
    distancias, indices = model_knn.kneighbors(vector_usuario, n_neighbors=10)
    
    # Recuperar los libros recomendados
    libros_recomendados = df_libros.iloc[indices.flatten()]
    
    return libros_recomendados[['Title', 'Author', 'genres']]

