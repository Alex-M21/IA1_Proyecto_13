# chat.py
from sentence_transformers import SentenceTransformer
import numpy as np
import json
import os

# Cargar el modelo
print("Cargando el modelo...")
model = SentenceTransformer('paraphrase-distilroberta-base-v1')  # Modelo más preciso
print("Modelo cargado con éxito.")

embeddings = []
example_texts = []
responses = []

# Verificar si los embeddings ya están guardados
embedding_file = "embeddings_data.npz"
if os.path.exists(embedding_file):
    # Cargar los embeddings precomputados desde el archivo
    print("Cargando embeddings precomputados desde el archivo...")
    data = np.load(embedding_file, allow_pickle=True)
    embeddings = data['embeddings']
    example_texts = data['example_texts']
    responses = data['responses']
    print("Embeddings cargados con éxito.")
else:
    # Cargar los datos de entrenamiento desde el archivo JSON
    print("Cargando datos de entrenamiento desde el archivo JSON...")
    with open("experimento.json", "r", encoding="utf-8") as file:
        intents = json.load(file)
    print("Datos cargados con éxito.")

    # Precomputar los embeddings para los ejemplos de entrenamiento
    print("Precomputando embeddings para los ejemplos de entrenamiento...")
    for intent in intents["intents"]:
        for example in intent["examples"]:
            vector = model.encode([example["userText"]])[0]  # Genera embedding para cada texto
            embeddings.append(vector)
            example_texts.append(example["userText"])
            responses.append(example["botResponse"])
            print(f"Embeddings calculados para: {example['userText']}")

    # Convertir la lista de embeddings a un arreglo de numpy para operaciones en batch
    embeddings = np.array(embeddings)

    # Guardar los embeddings en un archivo .npz para su uso posterior
    print("Guardando los embeddings precomputados...")
    np.savez_compressed(embedding_file, embeddings=embeddings, example_texts=example_texts, responses=responses)
    print("Embeddings guardados con éxito.")

# Función para calcular similitudes del coseno
def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Función para obtener la respuesta del bot
def get_bot_response(user_message):
    print(f"Calculando respuesta para: {user_message}")
    user_vector = model.encode([user_message])[0]

    # Calcular las similitudes del coseno con todos los embeddings precomputados
    similarities = np.array([cosine_similarity(user_vector, emb) for emb in embeddings])

    # Obtener el índice del ejemplo más similar
    best_match_idx = np.argmax(similarities)

    # Devolver siempre la respuesta correspondiente
    return responses[best_match_idx]
