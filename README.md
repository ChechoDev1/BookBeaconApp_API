# Sistema de Recomendación de Libros

Este proyecto implementa un sistema de recomendación de libros utilizando el lenguaje de programación Python y varias bibliotecas populares para análisis de datos y desarrollo web.

## Descripción
El sistema utiliza datos de Goodreads para recomendar libros basados en los géneros y autores favoritos de un usuario. Utiliza un modelo de vecinos más cercanos (KNN) para encontrar libros similares en función de la entrada del usuario. 
Además, se integra con Firebase para almacenar y recuperar información de usuarios.

## Componentes Principales
1. codigo.py - Generación de Recomendaciones
   Cargar los datos de Goodreads.
  Preprocesar y vectorizar los datos utilizando TF-IDF.
  Entrenar un modelo de vecinos más cercanos.
  Definir una función para recomendar libros basados en las preferencias del usuario.
2. main.py - Aplicación Web
   Este código implementa una aplicación web utilizando Flask. Incluye:
     Rutas para manejar las solicitudes del usuario, incluida una ruta para obtener recomendaciones de libros.
     Integración con el módulo de recomendaciones para proporcionar resultados personalizados a través de la interfaz web.
3. key.json - Clave de Firebase
   Se requiere una clave de Firebase para autenticar la aplicación y acceder a la base de datos de usuarios.
 

