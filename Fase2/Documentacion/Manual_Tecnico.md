# Manual Tecnico

1. [Introduccion](#introduccion)
2. [Estrcutura del proyecto](#estructura)
3. [Dependencias](#dependencias)
4. [Descripcion del codigo](#descripcion)
5. [Datos de entrenamiento](#datos)
6. [Despliegue](#despliegue)
7. [Estilos](#estilo)
7. [Limitaciones](#limitaciones)


### Introduccion <a name="sistema"></a>

Este manual describe el funcionamiento técnico de un chatbot avanzado desarrollado con React, TensorFlow.js y el modelo Universal Sentence Encoder (USE). El chatbot responde preguntas relacionadas con temas de alimentación y está diseñado para un despliegue web eficiente.

### Estrcutura del proyecto <a name="estructura"></a>

#### Archivos Principales

    - Chatbot.js: Componente React principal con la lógica del chatbot.

    - modelLoader.js: Carga del modelo y los datos de entrenamiento.

    - chat.css: Archivo de estilos para la interfaz.


### Dependencias <a name="dependencias"></a>

#### Bibliotecas Requeridas

- React: Framework para interfaces de usuario.

- TensorFlow.js: Biblioteca para el uso de modelos de IA en el navegador.

- Universal Sentence Encoder (USE): Modelo para representaciones vectoriales de texto.

#### Instalación de dependencias:
```bash
npm install react @tensorflow/tfjs @tensorflow-models/universal-sentence-encoder 
```

### Descripcion del codigo <a name="descripcion"></a>

#### Estados Principales

- inputText: Almacena el texto ingresado por el usuario.

- chatHistory: Historial de mensajes intercambiados.

- isBotTyping: Indica si el bot está escribiendo.

- isModelReady: Verifica si el modelo está cargado.
#### Carga del Modelo y Datos

Se utiliza useEffect para cargar el modelo y los datos de entrenamiento:


```bash
useEffect(() => {
  const initializeModel = async () => {
    const { model, embeddings } = await loadModelAndData();
    modelRef.current = model;
    embeddingsRef.current = embeddings;
    setIsModelReady(true);
  };

  initializeModel();
}, []);
```

#### Procesamiento de Entrada

El texto ingresado se compara con los ejemplos usando la distancia coseno:
```bash
const processInput = async (text) => {
  setIsBotTyping(true);

  if (!modelRef.current || embeddingsRef.current.length === 0) {
    setTimeout(() => {
      setChatHistory((prev) => [...prev, { sender: "bot", message: "Cargando..." }]);
      setIsBotTyping(false);
    }, 1000);
    return;
  }

  const inputEmbedding = await modelRef.current.embed([text]);
  const inputVector = inputEmbedding.arraySync()[0];

  const similarity = (a, b) => tf.losses.cosineDistance(a, b, 0).arraySync();
  let bestMatch = null;
  let lowestDistance = 1;

  for (const example of embeddingsRef.current) {
    const distance = similarity(inputVector, example.vector);
    if (distance < lowestDistance) {
      lowestDistance = distance;
      bestMatch = example.response;
    }
  }

  const botResponse = bestMatch || "Lo siento, no entendí eso.";
  setTimeout(() => {
    setChatHistory((prev) => [...prev, { sender: "bot", message: botResponse }]);
    setIsBotTyping(false);
  }, 2000);
};
```

#### Interfaz de Usuario

- Contenedor del chat: Muestra el historial de mensajes y el estado "escribiendo" del bot.

- Formulario de entrada: Permite al usuario ingresar texto y enviarlo.

```bash
<div className="chatContainer">
  <h2 className="header">Chatbot Multilingüe</h2>
  <div className="chatBox" ref={chatBoxRef}>
    {chatHistory.map((entry, index) => (
      <div key={index} className={entry.sender === "user" ? "userMessage" : "botMessage"}>
        <div className={entry.sender === "user" ? "userBubble" : "botBubble"}>
          <strong>{entry.sender === "user" ? "Tú" : "Bot"}:</strong> {entry.message}
        </div>
      </div>
    ))}

    {isBotTyping && (
      <div className="botMessage">
        <div className="botBubble">
          <strong>Bot:</strong> ...
        </div>
      </div>
    )}
  </div>
</div>
```

#### Datos de Entrenamiento

El archivo trainingData.json contiene intenciones y ejemplos en formato JSON:

```bash
{
  "intents": [
    {
      "intent": "saludo",
      "examples": [
        { "userText": "Hola", "botResponse": "¡Hola! ¿Cómo puedo ayudarte?" },
        { "userText": "Buenos días", "botResponse": "Buenos días, ¿en qué te puedo ayudar?" }
      ]
    }
  ]
}
```

### Despliegue <a name="despliegue"></a>

#### Requisitos

- Navegador moderno compatible con JavaScript.

- GitHub Pages configurado para el repositorio.

#### Pasos de Despliegue

- Subir el proyecto al repositorio de GitHub.

- Configurar GitHub Pages:

    - Ir a la configuración del repositorio.

    - Habilitar GitHub Pages en la rama principal.

- Acceso al chatbot: El chatbot estará disponible en la URL proporcionada por GitHub Pages.

### Estilos <a name="estilos"></a>

Los estilos definidos en chat.css controlan la apariencia de los elementos:
```bash
.container {
  max-width: 600px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

.chatBox {
  border: 1px solid #ccc;
  padding: 10px;
  max-height: 400px;
  overflow-y: auto;
}

.userBubble {
  background-color: #007bff;
  color: white;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 5px;
}

.botBubble {
  background-color: #f1f1f1;
  color: black;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 5px;
}
```

### Limitaciones <a name="limitaciones"></a>

- Capacidad básica para responder preguntas.

- Simulación de escritura mediante un retraso fijo.

- Respuestas limitadas a las intenciones definidas en el archivo trainingData.json.