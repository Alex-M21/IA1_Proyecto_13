from chat import get_bot_response  # Asegúrate de que el archivo 'chat.py' existe y tiene la función 'get_bot_response'
from tkinter import *
import json
import os
from PIL import Image, ImageTk

class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot Optimizado IA1")
        self.root.configure(bg="#FFF3E1")  # Tonos claros de naranja
        self.root.geometry("1000x700")  # Tamaño de la ventana ajustado
        self.root.resizable(True, True)  # Permitir redimensionar la ventanaz

        # Variables de usuario
        self.user_logged_in = False
        self.username = ""
        self.current_conversation = None  # Guardar la conversación actual
        self.conversations = {}  # Diccionario para guardar las conversaciones

        # Crear barra lateral de login y chat (similar a WhatsApp)
        self.main_frame = Frame(self.root, bg="#FFF3E1")  # Fondo claro en naranja
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar izquierdo
        self.sidebar = Frame(self.main_frame, bg="#FFCC80", width=220)  # Reducir ancho del sidebar
        self.sidebar.pack(side="left", fill="y")

        # Cargar y redimensionar la imagen de la mascota para el sidebar
        self.profile_image_sidebar = Image.open("../chat2/mascota.png")  # Asegúrate de que esta ruta sea correcta
        self.profile_image_sidebar = self.profile_image_sidebar.resize((80, 80), Image.Resampling.LANCZOS)
        self.profile_photo_sidebar = ImageTk.PhotoImage(self.profile_image_sidebar)

        # Imagen de mascota en el sidebar
        self.profile_label_sidebar = Label(self.sidebar, image=self.profile_photo_sidebar, bg="#FFCC80")
        self.profile_label_sidebar.pack(pady=20)

        # Campos de login en el sidebar
        self.carnet_label = Label(self.sidebar, text="Carnet", bg="#FFCC80", fg="white", font=("Arial", 12))
        self.carnet_label.pack(pady=5)
        self.carnet_entry = Entry(self.sidebar, font=("Arial", 12), width=18)
        self.carnet_entry.pack(pady=5)

        self.clave_label = Label(self.sidebar, text="Clave", bg="#FFCC80", fg="white", font=("Arial", 12))
        self.clave_label.pack(pady=5)
        self.clave_entry = Entry(self.sidebar, font=("Arial", 12), show="*", width=18)
        self.clave_entry.pack(pady=5)

        self.login_button = Button(self.sidebar, text="Iniciar Sesión", command=self.login, font=("Arial", 10),
                                   bg="#FF7043", fg="white")  # Reducir tamaño
        self.login_button.pack(pady=15)

        # Espacio para mostrar nombre de usuario después del login
        self.username_label = Label(self.sidebar, text="", bg="#FFCC80", fg="white", font=("Arial", 12))

        # Lista de conversaciones
        self.conversations_listbox = Listbox(self.sidebar, font=("Arial", 10), height=12,
                                             width=28)  # Reducir tamaño de la lista
        self.conversations_listbox.pack(pady=15)
        self.conversations_listbox.bind("<Double-1>", self.load_conversation_from_list)

        # Botón para eliminar una conversación
        self.delete_button = Button(self.sidebar, text="Borrar Conversación", command=self.delete_conversation,
                                    font=("Arial", 10), bg="#FF7043", fg="white")  # Reducir tamaño
        self.delete_button.pack(pady=5)

        # Botón de instrucciones
        self.instructions_button = Button(self.sidebar, text="Instrucciones", command=self.show_instructions,
                                          font=("Arial", 10), bg="#FF7043", fg="white")
        self.instructions_button.pack(pady=5)

        # Marco del área de chat
        self.chat_frame = Frame(self.main_frame, bg="#FFF3E1")
        self.chat_frame.pack(pady=0, padx=20, fill="both", expand=True)  # Ajustado el padding para ocupar más espacio

        self.scrollbar = Scrollbar(self.chat_frame)
        self.scrollbar.pack(side="right", fill="y")

        # Ajuste del tamaño de la letra del chat y colores
        self.chat_box = Text(self.chat_frame, wrap="word", yscrollcommand=self.scrollbar.set, state="disabled",
                             height=25, width=70, font=("Arial", 14), bg="#FFF3E1",
                             fg="#333")  # Aumentar tamaño del texto
        self.chat_box.pack()

        self.scrollbar.config(command=self.chat_box.yview)

        # Crear marco de entrada
        self.input_frame = Frame(self.main_frame, bg="#FFF3E1")
        self.input_frame.pack(pady=0)  # Eliminar padding extra

        self.input_field = Entry(self.input_frame, width=70,
                                 font=("Arial", 12))  # Ampliar input para que tenga el mismo ancho
        self.input_field.grid(row=0, column=0, padx=10, pady=10)
        self.input_field.bind("<Return>", self.send_message)

        self.send_button = Button(self.input_frame, text="Enviar", command=self.send_message, font=("Arial", 10),
                                  bg="#FF7043", fg="white")  # Reducir tamaño
        self.send_button.grid(row=0, column=1, padx=10)

        self.clear_button = Button(self.input_frame, text="Borrar Chat", command=self.clear_chat, font=("Arial", 10),
                                   bg="#FF7043", fg="white")  # Reducir tamaño
        self.clear_button.grid(row=1, column=0, columnspan=2, pady=5)

        self.save_button = Button(self.input_frame, text="Guardar Conversación", command=self.save_conversation,
                                  font=("Arial", 10), bg="#FF7043", fg="white")  # Reducir tamaño
        self.save_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Cargar las conversaciones previas desde el archivo JSON
        self.load_conversations()

    def login(self):
        carnet = self.carnet_entry.get().strip()
        clave = self.clave_entry.get().strip()

        if carnet != "" and clave != "":  # Carnet correcto
            self.username = carnet  # Nombre de usuario
            self.user_logged_in = True
            self.carnet_entry.delete(0, END)
            self.clave_entry.delete(0, END)
            self.username_label.config(text=f"Usuario: {self.username}")
            self.username_label.pack(pady=10)
            self.add_message("Bot", f"¡Hola, {self.username}! ¿En qué puedo ayudarte hoy?", "blue")
            self.current_conversation = {
                "title": self.username,
                "messages": [
                    {"sender": "Bot", "text": f"¡Hola, {self.username}! ¿En qué puedo ayudarte hoy?", "color": "blue"}]
            }
            self.update_conversation_listbox()
        else:
            self.add_message("Bot", "Credenciales incorrectas. Intenta nuevamente.", "blue")

    def add_message(self, sender, message, color="black"):
        self.chat_box.config(state="normal")
        if sender == "Bot":
            font = ("Arial", 14, "italic")  # Fuente en cursiva para el bot
            fg_color = color  # Azul por defecto para el bot
        else:
            font = ("Arial", 14)  # Fuente normal para el usuario
            fg_color = "black"  # Negro para el usuario

        self.chat_box.insert(END, f"{sender}: {message}\n", fg_color)
        self.chat_box.config(state="disabled")
        self.chat_box.see(END)

    def send_message(self, event=None):
        user_message = self.input_field.get().strip()
        if not user_message:
            return

        self.add_message("Tú", user_message, "black")
        self.input_field.delete(0, END)

        # Obtener respuesta del chatbot utilizando get_bot_response
        bot_response = get_bot_response(user_message)  # Aquí se llama la función para obtener la respuesta real
        self.add_message("Bot", bot_response, "blue")

        # Guardar el mensaje en la conversación actual
        if self.current_conversation is not None:
            self.current_conversation["messages"].append({"sender": "Tú", "text": user_message, "color": "black"})
            self.current_conversation["messages"].append({"sender": "Bot", "text": bot_response, "color": "blue"})

    def clear_chat(self):
        self.chat_box.config(state="normal")
        self.chat_box.delete(1.0, END)
        self.chat_box.config(state="disabled")

    def save_conversation(self):
        # Guardar conversación solo cuando se presiona el botón
        if self.current_conversation:
            title = self.current_conversation["title"]
            self.conversations[title] = self.current_conversation
            # Guardar la conversación en el archivo JSON
            with open("conversations.json", "w") as f:
                json.dump(self.conversations, f, indent=4)
            print("Conversación guardada correctamente.")
            self.update_conversation_listbox()  # Actualizar lista
        else:
            print("No hay conversación para guardar.")

    def load_conversations(self):
        # Cargar las conversaciones desde el archivo JSON
        if os.path.exists("conversations.json"):
            with open("conversations.json", "r") as f:
                self.conversations = json.load(f)
            # Mostrar las conversaciones en la lista
            self.update_conversation_listbox()
        else:
            self.conversations = {}

    def load_conversation_from_list(self, event):
        # Cargar la conversación seleccionada
        selected_conversation_title = self.conversations_listbox.get(self.conversations_listbox.curselection())
        self.current_conversation = self.conversations[selected_conversation_title]
        self.chat_box.config(state="normal")
        self.chat_box.delete(1.0, END)
        for message in self.current_conversation["messages"]:
            self.add_message(message["sender"], message["text"], message["color"])
        self.chat_box.config(state="disabled")

    def delete_conversation(self):
        # Eliminar la conversación seleccionada
        selected_conversation_title = self.conversations_listbox.get(self.conversations_listbox.curselection())
        del self.conversations[selected_conversation_title]

        # Guardar el archivo JSON después de eliminar
        with open("conversations.json", "w") as f:
            json.dump(self.conversations, f, indent=4)

        self.update_conversation_listbox()  # Actualizar lista después de eliminar
        print(f"Conversación '{selected_conversation_title}' eliminada.")

    def update_conversation_listbox(self):
        # Limpiar la lista y actualizarla con las conversaciones guardadas
        self.conversations_listbox.delete(0, END)
        for title in self.conversations:
            self.conversations_listbox.insert(END, title)

    def show_instructions(self):

        instructions = """Instrucciones de uso / Usage Instructions:
            1. Iniciar sesión con tu carnet y clave. / Log in with your ID card and password.
            2. Escribir tus mensajes en el campo de entrada. / Type your messages in the input field.
            3. El chatbot responderá automáticamente. / The chatbot will respond automatically.
            4. Puedes guardar y cargar tus conversaciones. / You can save and load your conversations.
            5. Para borrar una conversación, selecciona y presiona 'Borrar Conversación'. / To delete
               a conversation, select it and click 'Delete Conversation'.
            6. El chatbot puede hablar sobre temas de tecnología, programación y más. / The chatbot can
               talk about technology, programming, and more.
            7. Puedes pedir ejemplos de código en JavaScript o Python. / You can request code examples 
               in JavaScript or Python.
            8. También puede conversar sobre temas casuales como ejercicios y estaciones del año. / It 
               can also engage in casual conversations about topics like exercises and seasons of the year.
            9. Pregunta sobre cualquier tema y el chatbot te dará una respuesta relacionada. / Ask about
               any topic, and the chatbot will give you a related response.
               
               (Aveces el chatbot no reconoce tu pregunta por los signos "¿" "?"   si no responde adecuadamente
               trata de utilizar los signos de interrogacion, esto puede ayudar a solventar tu pregunta )"""

        instruction_window = Toplevel(self.root)
        instruction_window.title("Instrucciones")
        instruction_window.geometry("800x500")

        label = Label(instruction_window, text=instructions, font=("Arial", 12), justify=LEFT, padx=10, pady=10)
        label.pack(fill=BOTH, expand=True)


if __name__ == "__main__":
    print("Iniciando la interfaz de usuario...")
    root = Tk()
    app = ChatbotApp(root)
    print("Interfaz de usuario iniciada.")
    root.mainloop()
