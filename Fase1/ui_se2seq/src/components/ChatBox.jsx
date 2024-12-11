import React from 'react';
import './ChatBox.css'; // Agregar estilos

const ChatBox = ({ chatHistory, isLoading }) => {
  return (
    <div className="chat-box">
      {/* Mostrar historial de chat */}
      {chatHistory.map((message, index) => (
        <div key={index} className={`chat-message ${message.user ? 'user' : 'bot'}`}>
          <div className="message-header">
            <strong>{message.user ? 'Tú' : 'Bot'}</strong>
          </div>
          <div className="message-content">
            {message.user && <div className="user-message">{message.user}</div>}
            {message.bot && <div className="bot-message">{message.bot}</div>}
          </div>
        </div>
      ))}

      {/* Mostrar los tres puntos mientras se carga la respuesta del bot */}
      {isLoading && (
        <div className="bot-message">
          <span>...</span>
        </div>
      )}
    </div>
  );
};

export default ChatBox;
