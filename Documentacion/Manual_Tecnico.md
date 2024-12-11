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

Este manual describe el funcionamiento técnico de un chatbot básico desarrollado con React, TensorFlow.js, y el modelo Universal Sentence Encoder (USE). El chatbot está diseñado para responder consultas en base a datos de entrenamiento y puede desplegarse fácilmente en plataformas como GitHub Pages.

### Estrcutura del proyecto <a name="estructura"></a>

#### Archivos Principales

    - Chatbot.js: Componente React que contiene la lógica del chatbot.

    - chat.css: Archivo de estilos CSS para la interfaz.

    - trainingData.json: Archivo JSON con los datos de entrenamiento, incluyendo intenciones y ejemplos.


### Dependencias <a name="dependencias"></a>

#### Bibliotecas Requeridas

- React: Framework de JavaScript para la creación de interfaces de usuario.

- TensorFlow.js: Biblioteca para el uso de modelos de aprendizaje automático en el navegador.

- Universal Sentence Encoder (USE): Modelo para crear representaciones vectoriales de texto.

#### Instalación de dependencias:
```bash
npm install react @tensorflow/tfjs @tensorflow-models/universal-sentence-encoder 
```

### Descripcion del codigo <a name="descripcion"></a>

#### Estados Principales

- model: Almacena el modelo Universal Sentence Encoder cargado.

- inputText: Texto ingresado por el usuario.

- chatHistory: Historial de mensajes intercambiados.

- trainingData: Datos de entrenamiento cargados desde el archivo JSON.

- isBotTyping: Indica si el bot está "escribiendo" para simular el tiempo de respuesta.

#### Carga del Modelo y Datos

Se utiliza un efecto (useEffect) para cargar el modelo USE y los datos de entrenamiento al montar el componente:


```bash
useEffect(() => {
  const loadModel = async () => {
    const loadedModel = await use.load();
    setModel(loadedModel);
    const trainingDataFromFile = await fetch("/trainingData.json").then(response => response.json());
    setTrainingData(trainingDataFromFile.intents);
  };
  loadModel();
}, []);
```

#### Procesamiento de Entrada

El texto del usuario se convierte en un vector de incrustación y se calcula la similitud con los ejemplos de entrenamiento mediante la distancia coseno:
```bash
const processInput = async (text) => {
  const inputEmbedding = await model.embed([text]);
  const inputVector = inputEmbedding.arraySync()[0];

  let bestMatch = null;
  let lowestDistance = 1;

  for (const intent of trainingData) {
    for (const example of intent.examples) {
      const userTextEmbedding = await model.embed([example.userText]);
      const userTextVector = userTextEmbedding.arraySync()[0];
      const distance = similarity(inputVector, userTextVector);

      if (distance < lowestDistance) {
        lowestDistance = distance;
        bestMatch = example.botResponse;
      }
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
<div className="chatBox">
  {chatHistory.map((entry, index) => (
    <div
      key={index}
      className={entry.sender === "user" ? "userMessage" : "botMessage"}
    >
      <div
        className={entry.sender === "user" ? "userBubble" : "botBubble"}
      >
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