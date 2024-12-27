import numpy as np
import tensorflow as tf
import json
from tensorflow.keras.layers import Embedding, LSTM, Dense, Input, Dropout, Bidirectional, GRU
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
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
    embedding = Embedding(input_dim=vocab_size, output_dim=embedding_dim, mask_zero=True)(input_layer)

    # LSTM bidireccional para mejorar la captación de dependencias de largo alcance
    lstm = Bidirectional(LSTM(256, return_sequences=True, dropout=0.3, recurrent_dropout=0.3))(embedding)

    # Segunda capa LSTM bidireccional para mayor capacidad de aprendizaje
    lstm_2 = Bidirectional(LSTM(256, return_sequences=True, dropout=0.3, recurrent_dropout=0.3))(lstm)

    # Capa densa con regularización de Dropout
    dense = Dense(vocab_size, activation='softmax')(lstm_2)

    model = Model(inputs=input_layer, outputs=dense)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model


# Preprocesamiento de textos y secuencias
def preprocess_data(training_data):
    input_texts = [pair['input'].lower() for pair in training_data]
    target_texts = [pair['output'].lower() for pair in training_data]

    tokenizer = tf.keras.preprocessing.text.Tokenizer(filters='')
    tokenizer.fit_on_texts(input_texts + target_texts)

    input_sequences = tokenizer.texts_to_sequences(input_texts)
    target_sequences = tokenizer.texts_to_sequences(target_texts)

    max_len = max(max(len(seq) for seq in input_sequences), max(len(seq) for seq in target_sequences))
    input_sequences = pad_sequences(input_sequences, maxlen=max_len, padding='post')
    target_sequences = pad_sequences(target_sequences, maxlen=max_len, padding='post')

    target_sequences_one_hot = np.array(
        [to_categorical(seq, num_classes=len(tokenizer.word_index) + 1) for seq in target_sequences])

    return tokenizer, input_sequences, target_sequences_one_hot, max_len


# Cargar datos preprocesados
tokenizer, input_sequences, target_sequences_one_hot, max_len = preprocess_data(training_data)

# Cargar el modelo si existe
model = load_model_from_file()

if model is None:
    model = create_model(input_shape=(max_len,), vocab_size=len(tokenizer.word_index) + 1)


# Función para predecir la respuesta del chatbot
def chat_with_bot(input_text):
    input_seq = tokenizer.texts_to_sequences([input_text.lower()])
    input_seq = pad_sequences(input_seq, maxlen=max_len, padding='post')

    prediction = model.predict(input_seq)
    predicted_sequence = np.argmax(prediction, axis=-1)[0]
    print("Predicted sequence indices:", predicted_sequence)

    response = []
    for word_index in predicted_sequence:
        if word_index == 0:
            break
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

    input_sequences = pad_sequences(input_sequences, maxlen=max_len, padding='post')
    target_sequences = pad_sequences(target_sequences, maxlen=max_len, padding='post')

    target_sequences_one_hot = np.array(
        [to_categorical(seq, num_classes=len(tokenizer.word_index) + 1) for seq in target_sequences]
    ) if len(target_sequences) > 0 else []

    # Callback para guardar el mejor modelo
    checkpoint_callback = ModelCheckpoint(
        filepath='best_model.keras',  # Cambiado a .keras
        save_best_only=True,
        monitor='val_loss',  # O cualquier métrica de validación que estés utilizando
    )

    # Ajuste para dividir datos de validación
    validation_split = 0.2  # Usar 20% para validación
    model.fit(
        input_sequences,
        target_sequences_one_hot,
        epochs=epochs,
        batch_size=1,
        validation_split=validation_split,
        callbacks=[checkpoint_callback]
    )
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
            epochs = input(
                "¿Cuántas épocas quieres entrenar el modelo? (Por ejemplo: 10 o escribe 'salir' para volver al menú): ")
            if epochs.lower() == 'salir':
                break
            if epochs.isdigit() and int(epochs) > 0:
                epochs = int(epochs)
                train_model(epochs)
                break
            else:
                print("Por favor, ingresa un número válido de épocas (mayor que 0) o escribe 'salir'.")
    elif option == '3':
        while True:
            user_input = input("Tú: ")
            if user_input.lower() == 'salir':
                break
            bot_response = chat_with_bot(user_input)
            print(f"Bot: {bot_response}")

    elif option == '4':
        save_model(model)

    elif option == '5':
        print("¡Hasta luego!")
        break
