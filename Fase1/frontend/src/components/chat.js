import React, { useState, useEffect } from "react";
import * as tf from "@tensorflow/tfjs";
import * as use from "@tensorflow-models/universal-sentence-encoder";
import './chat.css';

const Chatbot = () => {
  const [model, setModel] = useState(null);
  const [inputText, setInputText] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [trainingData, setTrainingData] = useState([]);

  // Cargar el modelo USE
  useEffect(() => {
    const loadModel = async () => {
      console.log("Cargando modelo...");
      const loadedModel = await use.load();
      setModel(loadedModel);
      console.log("Modelo cargado.");

      // Cargar datos de entrenamiento desde el archivo JSON
      const trainingDataFromFile = await fetch("/trainingData.json").then(response => response.json());
      setTrainingData(trainingDataFromFile.intents);  // Solo tomamos las intenciones
    };

    loadModel();
  }, []);

  // Procesar el texto de entrada
  const processInput = async (text) => {
    if (!model) {
      const loadingMessage = "El modelo aún se está cargando...";
      setChatHistory((prev) => [...prev, { sender: "bot", message: loadingMessage }]);
      return;
    }

    const inputEmbedding = await model.embed([text]);
    const inputVector = inputEmbedding.arraySync()[0];

    // Calcular similitud con ejemplos de entrenamiento
    const similarity = (a, b) => tf.losses.cosineDistance(a, b, 0).arraySync();
    let bestMatch = null;
    let lowestDistance = 1; // Distancia más baja

    // Iterar sobre las intenciones y ejemplos
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

    // Si no hay coincidencias cercanas, devolver una respuesta predeterminada
    const botResponse = bestMatch || "Lo siento, no entendí eso.";
    setChatHistory((prev) => [...prev, { sender: "bot", message: botResponse }]);
  };

  // Manejar el envío del texto
  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputText.trim() === "") return;

    // Registrar mensaje del usuario
    setChatHistory((prev) => [...prev, { sender: "user", message: inputText }]);

    processInput(inputText);
    setInputText(""); // Limpiar campo de entrada
  };

  return (
    <div className="container">
    <div className="chatContainer">
      <h2 className="header">Chatbot Multilingüe</h2>
      <div className="chatBox">
        {chatHistory.map((entry, index) => (
          <div
            key={index}
            className={entry.sender === "user" ? "userMessage" : "botMessage"}
          >
            <div className={entry.sender === "user" ? "userBubble" : "botBubble"}>
              <strong>{entry.sender === "user" ? "Tú" : "Bot"}:</strong> {entry.message}
            </div>
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="form">
      <input
        type="text"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="Escribe algo..."
        className="input"
      />
      <button type="submit" className="sendButton">
        Enviar
      </button>
    </form>
    </div>

   
  </div>
  );
};

export default Chatbot;
