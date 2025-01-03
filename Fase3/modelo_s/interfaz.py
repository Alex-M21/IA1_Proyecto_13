import tkinter as tk
import tkinter.font as tkFont


class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#D3D3D3")  # Fondo principal (gris claro)
        self.root.title("Chat - Inteligencia Artificial 1")
        self.root.geometry("600x400")

        # Configurar diseño responsivo
        self.root.rowconfigure(0, weight=0)  # Barra superior
        self.root.rowconfigure(1, weight=1)  # Caja de mensajes
        self.root.rowconfigure(2, weight=0)  # Entrada y botón
        self.root.columnconfigure(0, weight=1)

        # Barra superior
        self.title_frame = tk.Frame(root, bg="#2C3E50", height=40)
        self.title_frame.grid(row=0, column=0, sticky="ew")
        self.title_label = tk.Label(
            self.title_frame, text="Chatbot Multilingüe",
            bg="#2C3E50", fg="#FFFFFF", font=("Arial", 14, "bold")
        )
        self.title_label.pack(pady=5)

        # Área de mensajes con scrollbar
        self.chat_frame = tk.Frame(root, bg="#D3D3D3")
        self.chat_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.chat_canvas = tk.Canvas(self.chat_frame, bg="#D3D3D3", highlightthickness=0)
        self.chat_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(self.chat_frame, orient="vertical", command=self.chat_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.messages_frame = tk.Frame(self.chat_canvas, bg="#D3D3D3")
        self.chat_canvas.create_window((0, 0), window=self.messages_frame, anchor="nw")
        self.messages_frame.bind("<Configure>", lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))

        # Frame para entrada de texto y botón
        self.input_frame = tk.Frame(root, bg="#D3D3D3")
        self.input_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.input_frame.columnconfigure(0, weight=1)

        # Entrada de texto
        self.entry = tk.Entry(self.input_frame, font=("Arial", 12), bg="#FFFFFF", fg="#000000")
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<Return>", self.send_message)

        # Botón de enviar
        self.send_button = tk.Button(
            self.input_frame, text="Enviar", command=self.send_message,
            bg="#2C3E50", fg="#FFFFFF", font=("Arial", 12, "bold")
        )
        self.send_button.grid(row=0, column=1, padx=(5, 0))
        self.add_message("IA", "Hola, soy BotIA1 y estaré aquí ayudándote con temas de alimentación.", user=False)

    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if user_input:
            self.add_message("Tú", user_input, user=True)
            self.entry.delete(0, tk.END)
            response = self.get_response(user_input)
            self.add_message("IA", response, user=False)

    def add_message(self, sender, message, user=True):
        # Crear un frame para cada mensaje
        frame = tk.Frame(self.messages_frame, bg="#D3D3D3", pady=5)

        if user:
            frame.pack(anchor="e", padx=(50, 10))
        else:
            frame.pack(anchor="w", padx=(10, 50))

        # Crear fuente para medir el texto
        text_font = tk.font.Font(family="Arial", size=12)
        
        # Medir ancho y altura del texto
        text_width = min(text_font.measure(message), 380) + 20  # Máximo de 380 px + margen
        text_height = (message.count("\n") + 1) * text_font.metrics("linespace") + 20  # Líneas * altura + margen

        # Crear canvas para el óvalo del fondo
        canvas = tk.Canvas(frame, width=text_width+50, height=text_height+20, bg="#D3D3D3", highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.create_oval(5, 5, text_width - 5, text_height - 5, 
                        fill="#ADD8E6" if user else "#FFFFFF", 
                        outline="#ADD8E6" if user else "#CCCCCC")

        # Texto del mensaje
        text = tk.Label(canvas, text=f"{sender}: {message}", bg="#ADD8E6" if user else "#FFFFFF", 
                        font=("Arial", 12), wraplength=380, justify="left")
        text.place(x=10, y=10)

        # Actualizar el área de scroll
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1)


    def get_response(self, user_input):
        return "Respuesta simulada del modelo"

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
