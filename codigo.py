import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar la app de Firebase si aún no está inicializada
if not firebase_admin._apps:
    cred = credentials.Certificate("key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Función para obtener los géneros y autores favoritos del usuario autenticado
def obtener_preferencias_usuario(uid):
    usuario_ref = db.collection('users').document(uid)
    usuario = usuario_ref.get()
    if usuario.exists:
        datos_usuario = usuario.to_dict()
        generos_favoritos = datos_usuario.get('genres', '').split(';')
        autores_favoritos = datos_usuario.get('authors', '').split(';')
        return generos_favoritos, autores_favoritos
    else:
        return [], []

# Cargar el conjunto de datos
df = pd.read_csv('Goodreads_books_with_genres_simplificado.csv')
df = df[df['num_pages'] != 0]
df = df.dropna()
df['text'] = df['genres'] + ';' + df['Author']

# Vectorización
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['text'])

# Modelo de vecinos más cercanos
model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
model_knn.fit(tfidf_matrix)

def recomendar_libros(uid):
    # Obtener los géneros y autores favoritos del usuario
    generos_favoritos, autores_favoritos = obtener_preferencias_usuario(uid)
    
    # Crear el texto de entrada del usuario
    texto_usuario = ';'.join(generos_favoritos + autores_favoritos)
    
    # Convertir el texto del usuario en un vector TF-IDF
    vector_usuario = vectorizer.transform([texto_usuario])
    
    # Encontrar los vecinos más cercanos
    distancias, indices = model_knn.kneighbors(vector_usuario, n_neighbors=30)
    
    # Recuperar los libros recomendados
    libros_recomendados = df.iloc[indices.flatten()]
    
    return libros_recomendados[['Title', 'Author', 'genres']].to_dict('records')

