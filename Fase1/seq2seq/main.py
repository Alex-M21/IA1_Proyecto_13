import numpy as np
import tensorflow as tf
import json
from tensorflow.keras.layers import Embedding, LSTM, Dense, Input
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

# Cargar o inicializar datos de entrenamiento desde JSON
def load_training_data(file_path='training_data.json'):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_training_data(training_data, file_path='training_data.json'):
    with open(file_path, 'w') as file:
        json.dump(training_data, file, indent=4)

# Guardar el modelo
def save_model(model, filename='chatbot_model.h5'):
    model.save(filename)
    print(f"Modelo guardado en {filename}")

# Cargar el modelo
def load_model_from_file(filename='chatbot_model.h5'):
    try:
        model = tf.keras.models.load_model(filename)
        print(f"Modelo cargado desde {filename}")
        return model
    except OSError:
        print(f"No se pudo cargar el modelo desde {filename}. Se entrenará un nuevo modelo.")
        return None

# Inicializar datos de entrenamiento
training_data = load_training_data()

# Definir el modelo
def create_model(input_shape=(9,), vocab_size=1000, embedding_dim=128, target_len=9):
    input_layer = Input(shape=input_shape)
    embedding = Embedding(input_dim=vocab_size, output_dim=embedding_dim)(input_layer)
    lstm = LSTM(256, return_sequences=True)(embedding)
    lstm_2 = LSTM(256, return_sequences=True)(lstm)
    dense = Dense(vocab_size, activation='softmax')(lstm_2)

    model = Model(inputs=input_layer, outputs=dense)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Tokenización y padding
tokenizer = tf.keras.preprocessing.text.Tokenizer()
input_texts = [pair['input'] for pair in training_data]
target_texts = [pair['output'] for pair in training_data]
tokenizer.fit_on_texts(input_texts + target_texts)
input_sequences = tokenizer.texts_to_sequences(input_texts)
target_sequences = tokenizer.texts_to_sequences(target_texts)

# Ajustar la longitud máxima de entrada y salida
max_input_len = max(len(seq) for seq in input_sequences) if input_sequences else 9
max_target_len = max(len(seq) for seq in target_sequences) if target_sequences else 9

input_sequences = pad_sequences(input_sequences, maxlen=max_input_len, padding='post')
target_sequences = pad_sequences(target_sequences, maxlen=max_input_len, padding='post')  # Ajustar aquí

# Convertir las secuencias de destino a one-hot encoding
target_sequences_one_hot = np.array(
    [to_categorical(seq, num_classes=len(tokenizer.word_index) + 1) for seq in target_sequences]
) if len(target_sequences) > 0 else []

# Cargar el modelo si existe
model = load_model_from_file()

if model is None:
    # Si el modelo no se encuentra, se crea uno nuevo
    model = create_model(input_shape=(max_input_len,), vocab_size=len(tokenizer.word_index) + 1, target_len=max_input_len)

# Función para predecir la respuesta del chatbot
def chat_with_bot(input_text):
    input_seq = tokenizer.texts_to_sequences([input_text])
    input_seq = pad_sequences(input_seq, maxlen=max_input_len, padding='post')

    prediction = model.predict(input_seq)
    predicted_sequence = np.argmax(prediction, axis=-1)[0]

    response = []
    for word_index in predicted_sequence:
        for word, index in tokenizer.word_index.items():
            if index == word_index:
                response.append(word)
                break
    return ' '.join(response)

# Función para entrenar el modelo
def train_model(epochs=10):
    global model
    input_texts = [pair['input'] for pair in training_data]
    target_texts = [pair['output'] for pair in training_data]

    tokenizer.fit_on_texts(input_texts + target_texts)
    input_sequences = tokenizer.texts_to_sequences(input_texts)
    target_sequences = tokenizer.texts_to_sequences(target_texts)

    input_sequences = pad_sequences(input_sequences, maxlen=max_input_len, padding='post')
    target_sequences = pad_sequences(target_sequences, maxlen=max_input_len, padding='post')

    target_sequences_one_hot = np.array(
        [to_categorical(seq, num_classes=len(tokenizer.word_index) + 1) for seq in target_sequences]
    ) if len(target_sequences) > 0 else []

    model.fit(input_sequences, target_sequences_one_hot, epochs=epochs, batch_size=1)
    print(f"Entrenamiento completado por {epochs} épocas.")

    # Guardar el modelo después de entrenar
    save_model(model)

# Menú interactivo
while True:
    print("\n=== MENÚ PRINCIPAL ===")
    print("1. Agregar datos de entrenamiento")
    print("2. Entrenar el modelo")
    print("3. Chatear con el chatbot")
    print("4. Guardar el modelo actual")
    print("5. Salir")

    option = input("Selecciona una opción: ")

    if option == '1':
        while True:
            entry = input("Escribe una entrada (o 'salir' para terminar): ")
            if entry.lower() == 'salir':
                break
            response = input("Escribe la respuesta correspondiente: ")
            training_data.append({'input': entry, 'output': response})
            save_training_data(training_data)

    elif option == '2':
        while True:
            epochs = input("¿Cuántas épocas quieres entrenar el modelo? (Por ejemplo: 10): ")
            try:
                epochs = int(epochs)
                train_model(epochs)
                break
            except ValueError:
                print("Por favor, ingresa un número válido de épocas.")

    elif option == '3':
        while True:
            user_input = input("Tú: ")
            if user_input.lower() == 'salir':
                break
            bot_response = chat_with_bot(user_input)
            print(f"Bot: {bot_response}")

    elif option == '4':
        save_model(model)
        print("Modelo guardado con éxito.")

    elif option == '5':
        print("¡Hasta luego!")
        break
