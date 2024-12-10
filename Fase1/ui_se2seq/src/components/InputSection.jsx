import React from 'react';
import './InputSection.css';

const InputSection = ({ input, onInputChange, onSendMessage }) => {
  return (
    <div className="input-section">
      <input
        type="text"
        value={input}
        onChange={onInputChange}
        placeholder="Escribe un mensaje..."
      />
      <button onClick={onSendMessage}>Enviar</button>
    </div>
  );
};

export default InputSection;
