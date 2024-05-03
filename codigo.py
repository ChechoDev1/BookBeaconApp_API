import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    # Inicializar Firebase
    cred = credentials.Certificate("key.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

# Cargar el conjunto de datos
df = pd.read_csv('Goodreads_books_with_genres_simplificado.csv')
df = df[df['num_pages'] != 0]
df = df.dropna()
# Combinar géneros y autores en una sola columna
df['text'] = df['genres'] + ';' + df['Author']

# Vectorización
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['text'])

# Modelo de vecinos más cercanos
model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
model_knn.fit(tfidf_matrix)

def obtener_preferencias_usuario(uid):
    # Obtener los datos del usuario desde Firestore
    doc_ref = db.collection('users').document(uid)
    doc = doc_ref.get().to_dict()
    if doc:
        genres = doc.get('genres', [])
        authors = doc.get('authors', [])
        print("Preferencias de géneros:", genres)
        print("Preferencias de autores:", authors)
        return doc.get('genres', []), doc.get('authors', [])
    else:
        return [], []

def recomendar_libros(uid):
    # Obtener las preferencias del usuario
    generos_favoritos, autores_favoritos = obtener_preferencias_usuario(uid)
    
    # Crear el texto de entrada del usuario
    texto_usuario = ';'.join(generos_favoritos + autores_favoritos)
    
    # Convertir el texto del usuario en un vector TF-IDF
    vector_usuario = vectorizer.transform([texto_usuario])
    
    # Encontrar los vecinos más cercanos
    distancias, indices = model_knn.kneighbors(vector_usuario, n_neighbors=10)
    
    # Recuperar los libros recomendados
    libros_recomendados = df.iloc[indices.flatten()]
    
    # Convertir el DataFrame a una lista de diccionarios
    libros_recomendados_dict = libros_recomendados[['Title', 'Author', 'genres']].to_dict('records')
    
    return libros_recomendados_dict



