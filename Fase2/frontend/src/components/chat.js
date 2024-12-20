import React, { useState, useEffect, useRef } from "react";
import * as tf from "@tensorflow/tfjs";
import { loadModelAndData } from "./modelLoader"; // Importa el módulo creado
import './chat.css';

const Chatbot = () => {
  const [inputText, setInputText] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [isBotTyping, setIsBotTyping] = useState(false);
  const [isModelReady, setIsModelReady] = useState(false);

  const modelRef = useRef(null);
  const embeddingsRef = useRef([]);
  const chatBoxRef = useRef(null);

  useEffect(() => {
    const initializeModel = async () => {
      const { model, embeddings } = await loadModelAndData();
      modelRef.current = model;
      embeddingsRef.current = embeddings;
      setIsModelReady(true); // Marca el modelo como listo
    };

    initializeModel();
  }, []);

  useEffect(() => {
    const welcomeMessage = "¡Hola! Soy tu chat virtual. Puedo ayudarte con temas de, cine, entretenimiento, gym, comida, tecnología, estaciones del año, clima, bromas. ¿De qué quieres hablar?";
    let currentText = "";
    let index = 0;

    const typeMessage = () => {
      if (index < welcomeMessage.length) {
        currentText += welcomeMessage[index];
        setChatHistory((prev) => [
          ...prev.filter((entry) => entry.sender !== "bot"), // Eliminar mensaje parcial anterior
          { sender: "bot", message: currentText },
        ]);
        index++;
        setTimeout(typeMessage, 100); //(100ms por letra)
      }
    };

    typeMessage();
  }, []);

  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [chatHistory, isBotTyping]);

  const processInput = async (text) => {
    setIsBotTyping(true);

    if (!modelRef.current || embeddingsRef.current.length === 0) {
      setTimeout(() => {
        setChatHistory((prev) => [
          ...prev,
          { sender: "bot", message: "cargando..." },
        ]);
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

    const typingDelay = Math.min(800 + botResponse.length * 20, 2000);
    setTimeout(() => {
      setChatHistory((prev) => [
        ...prev,
        { sender: "bot", message: botResponse },
      ]);
      setIsBotTyping(false);
    }, typingDelay);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputText.trim() === "") return;

    setChatHistory((prev) => [...prev, { sender: "user", message: inputText }]);
    processInput(inputText);
    setInputText("");
  };

  return (
    <div className="container">
      <header className="mainHeader">
        <h1>
          Chatbot Optimizado IA1
          <span
            style={{
              display: "inline-block",
              width: "12px",
              height: "12px",
              marginLeft: "10px",
              borderRadius: "50%",
              backgroundColor: isModelReady ? "green" : "red",
            }}
            title={isModelReady ? "Modelo listo" : "Cargando modelo..."}
          ></span>
        </h1>
      </header>

      <div className="chatContainer">
        <h2 className="header">Chatbot Multilingüe</h2>
        <div className="chatBox" ref={chatBoxRef}>
          {chatHistory.map((entry, index) => (
            <div
              key={index}
              className={entry.sender === "user" ? "userMessage" : "botMessage"}
            >
              <div
                className={entry.sender === "user" ? "userBubble" : "botBubble"}
              >
                <strong>{entry.sender === "user" ? "Tú" : "Bot"}:</strong>{" "}
                {entry.message}
              </div>
            </div>
          ))}

          {isBotTyping && (
            <div className="botMessage">
              <div className="botBubble">
                <strong>Bot:</strong>{" "}
                <span className="typingIndicator">...</span>
              </div>
            </div>
          )}
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
