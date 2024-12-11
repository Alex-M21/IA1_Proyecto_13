import React, { useState, useEffect } from 'react';
import * as tf from '@tensorflow/tfjs';
import './App.css';
import ChatBox from './components/ChatBox';
import InputSection from './components/InputSection';

function App() {
  const [model, setModel] = useState(null);
  const [input, setInput] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false); // Estado para controlar la carga

  useEffect(() => {
    const loadModel = async () => {
      try {
        // Cargar el modelo de TensorFlow.js
        const loadedModel = await tf.loadLayersModel('/tfjs_model_chat/model.json');
        setModel(loadedModel);
      } catch (error) {
        console.error('Error al cargar el modelo:', error);
        setChatHistory((prevChatHistory) => [
          ...prevChatHistory,
          { user: '', bot: 'Hubo un problema al cargar el modelo. Intenta más tarde.' }
        ]);
      }
    };

    loadModel();
  }, []);

  const handleInputChange = (event) => {
    setInput(event.target.value);
  };

  const handleSendMessage = async () => {
    if (model && input.trim() !== '') {
      // Agregar mensaje del usuario al historial
      setChatHistory((prevChatHistory) => [
        ...prevChatHistory,
        { user: input, bot: '' }, // El bot aún no ha respondido
      ]);
      setInput(''); // Limpiar el campo de entrada
      setIsLoading(true); // Mostrar el indicador de carga

      try {
        const inputTensor = preprocessInput(input); // Preprocesar la entrada
        const response = await model.predict(inputTensor); // Obtener respuesta del modelo
        const responseText = decodeResponse(response); // Decodificar la respuesta

        // Agregar respuesta del bot al historial
        setChatHistory((prevChatHistory) => {
          const newChatHistory = [...prevChatHistory];
          newChatHistory[newChatHistory.length - 1].bot = responseText;
          return newChatHistory;
        });
      } catch (error) {
        console.error('Error al procesar el mensaje:', error);
        // Si ocurre un error en la predicción, el bot responde con un mensaje genérico
        setChatHistory((prevChatHistory) => [
          ...prevChatHistory,
          { user: input, bot: 'Hola, no entendí. ¿Puedes repetirlo?' },
        ]);
      } finally {
        setIsLoading(false); // Ocultar el indicador de carga
      }
    }
  };

  const preprocessInput = (input) => {
    // Convertir la entrada en un tensor (ajusta según la tokenización de tu modelo)
    return tf.tensor([input.split('').map((char) => char.charCodeAt(0))]);
  };

  const decodeResponse = (response) => {
    const responseArray = response.dataSync ? response.dataSync() : [];
    return String.fromCharCode(...responseArray);
  };

  return (
    <div className="App">
      <div className="chat-container">
        <h2 className="chat-header">Chat Multilingüe</h2>
        <ChatBox chatHistory={chatHistory} isLoading={isLoading} />
        <InputSection
          input={input}
          onInputChange={handleInputChange}
          onSendMessage={handleSendMessage}
        />
      </div>
    </div>
  );
}

export default App;
