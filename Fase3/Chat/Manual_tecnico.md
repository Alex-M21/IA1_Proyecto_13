# Manual Técnico: Chatbot Optimizado IA1

## Introducción
Este manual técnico está diseñado para proporcionar una comprensión completa del funcionamiento interno del chatbot IA1. Incluye una descripción detallada de los módulos, funciones, y la lógica detrás del sistema, así como los archivos creados durante la ejecución.

---

## Componentes Principales

### 1. `chat.py`
Este archivo contiene la lógica principal para la interacción del chatbot, desde cargar el modelo hasta generar respuestas.

#### a. **Cargar el modelo**
```python
model = SentenceTransformer('paraphrase-distilroberta-base-v1')
```
- **Función**: Carga un modelo preentrenado de SentenceTransformers para calcular representaciones vectoriales de textos (embeddings).
- **Modelo utilizado**: `paraphrase-distilroberta-base-v1`.
- **Propósito**: Proporcionar embeddings que capturen el significado semántico de las entradas del usuario.

#### b. **Embeddings y datos precomputados**
```python
embedding_file = "embeddings_data.npz"
```
- **Descripción**: Archivo comprimido que contiene los embeddings precomputados, ejemplos de texto y respuestas.
- **Lógica**:
  1. Si existe el archivo, se cargan los datos precomputados.
  2. Si no, se calculan embeddings desde un archivo JSON de intenciones y se guardan en `embeddings_data.npz`.

#### c. **Funciones principales**

##### i. `cosine_similarity(vec1, vec2)`
- **Entrada**: Dos vectores.
- **Salida**: Similitud del coseno entre ambos vectores.
- **Uso**: Medir la similitud entre el mensaje del usuario y los ejemplos precomputados.

##### ii. `get_bot_response(user_message)`
- **Entrada**: Un mensaje del usuario.
- **Salida**: Respuesta más adecuada del chatbot.
- **Proceso**:
  1. Convierte el mensaje del usuario a un vector mediante el modelo.
  2. Calcula la similitud del coseno con todos los embeddings precomputados.
  3. Selecciona el índice del ejemplo más similar y devuelve la respuesta correspondiente.

---

### 2. `inter.py`
Proporciona la interfaz gráfica para interactuar con el chatbot.

#### a. **Funciones principales**

##### i. `save_conversation()`
- **Descripción**: Guarda la conversación actual en `conversations.json`.
- **Lógica**:
  1. Carga las conversaciones existentes desde el archivo.
  2. Añade la nueva conversación.
  3. Sobrescribe el archivo con las conversaciones actualizadas.

##### ii. `load_conversations()`
- **Descripción**: Carga y muestra las conversaciones guardadas.
- **Proceso**:
  1. Lee el archivo `conversations.json`.
  2. Actualiza la lista de conversaciones en la interfaz.

##### iii. `show_instructions()`
- **Descripción**: Muestra instrucciones en un cuadro de diálogo.
- **Personalización**: Incluye temas de conversación y ejemplos de uso.

---

## Modelo de Aprendizaje Automático
- **Tipo de modelo**: Sentence-BERT (SBERT).
- **Función**: Convierte frases a embeddings que capturan relaciones semánticas.
- **Ventajas**:
  - Alta precisión para tareas de similitud textual.
  - Eficiente en términos de tiempo y recursos.

---

## Archivos Generados

### 1. `embeddings_data.npz`
- **Contenido**:
  - `embeddings`: Vectores de características de ejemplos de texto.
  - `example_texts`: Frases de entrenamiento.
  - `responses`: Respuestas predefinidas del chatbot.

### 2. `conversations.json`
- **Contenido**: Historias completas de interacciones entre el usuario y el chatbot.
- **Uso**: Permite al usuario revisar conversaciones pasadas.

### 3. `mascota.png`
- **Propósito**: Archivo de imagen utilizado en la interfaz gráfica.

---

## Flujo de Datos
1. **Carga inicial**:
   - Verifica la existencia de datos precomputados.
   - Si no existen, calcula y guarda los embeddings.

2. **Interacción con el usuario**:
   - Recibe un mensaje del usuario.
   - Calcula la similitud con ejemplos.
   - Devuelve la respuesta correspondiente.

3. **Gestión de conversaciones**:
   - Guarda y carga interacciones a través de la interfaz.

---

## Solución de Problemas

### Problema: No se guardan los embeddings
- **Causa posible**: Falta de permisos para escribir en el directorio.
- **Solución**: Verificar permisos de escritura y reintentar.

### Problema: Respuesta incorrecta del chatbot
- **Causa posible**: Ejemplos de entrenamiento insuficientes.
- **Solución**: Ampliar el archivo JSON con más ejemplos relevantes.

---

## Contacto y Soporte
Para consultas técnicas o soporte, contacta a: **soporte@chatbot-ia1.com**.
