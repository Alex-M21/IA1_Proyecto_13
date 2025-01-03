import tkinter as tk
from tkinter import scrolledtext
from transformers import AutoTokenizer, AutoModelForCausalLM

# Cargar modelo y tokenizer
tokenizer = AutoTokenizer.from_pretrained("trained_model")
model = AutoModelForCausalLM.from_pretrained("trained_model")

def generate_response(user_input):
    inputs = tokenizer(user_input, return_tensors="pt", truncation=True)
    outputs = model.generate(
    inputs.input_ids,
    max_length=150,
    num_return_sequences=1,
    pad_token_id=tokenizer.eos_token_id,
    temperature=0.7,  # Reduce la determinación (ajustable)
    top_k=50,         # Limita las opciones más probables
    top_p=0.9,        # Filtra tokens acumulativos dentro del 90% de probabilidad
    repetition_penalty=1.2  # Penaliza la repetición de palabras
)

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

def send_message(event=None):
    user_message = input_box.get("1.0", tk.END).strip()
    if user_message:
        chat_area.config(state=tk.NORMAL)

        chat_area.insert(tk.END, f"Usuario: {user_message}\n", "user_tag")


        input_box.delete("1.0", tk.END)
        
        # Obtener respuesta del modelo
        chatbot_response = generate_response(user_message)

        chat_area.insert(tk.END, "Chatbot: ", "bot_tag")
        chat_area.insert(tk.END, f"{chatbot_response}\n")
        
        chat_area.config(state=tk.DISABLED)
        chat_area.see(tk.END)

root = tk.Tk()
root.title("Chatbot")
root.geometry("600x700")
root.configure(bg="#2F2F2F")  # Gris oscuro de fondo

title_label = tk.Label(root, text="Chatbot", font=("Helvetica", 18, "bold"), bg="#444444", fg="white")
title_label.pack(fill=tk.X, pady=10)

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12), bg="#555555", fg="#D3D3D3")
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_area.config(state=tk.DISABLED)

chat_area.tag_config("user_tag", font=("Arial", 12, "bold"), foreground="#FFFFFF")
chat_area.tag_config("bot_tag", font=("Arial", 12), foreground="#D3D3D3")

input_box = tk.Text(root, height=3, font=("Arial", 12), bg="#444444", fg="#D3D3D3", insertbackground="#D3D3D3")
input_box.pack(padx=10, pady=(0, 10), fill=tk.X)

send_button = tk.Button(root, text="Enviar", font=("Arial", 12, "bold"), bg="#3498DB", fg="#2C3E50", command=send_message)
send_button.pack(pady=(0, 20))

root.bind("<Return>", send_message)

root.mainloop()
