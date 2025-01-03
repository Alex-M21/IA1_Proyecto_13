# Manual de Usuario: Chatbot Optimizado IA1

## Introducción
Este chatbot ha sido diseñado para interactuar con los usuarios en temas de tecnología, programación, ejemplos de código en JavaScript y Python, además de mantener conversaciones casuales sobre ejercicios y estaciones del año.

## Requisitos del Sistema

- Python 3.8 o superior.
- Librerías necesarias:
  - tkinter
  - json
  - os
  - PIL (Pillow)
- Archivo de imagen: `mascota.png` (para el sidebar).
- Archivo `conversations.json` para almacenar conversaciones.

## Instrucciones de Uso

### 1. Inicio de sesión
1. Introduce tu **carnet** y **clave** en los campos correspondientes del sidebar.
2. Haz clic en el botón **Iniciar Sesión**.
3. Una vez autenticado, aparecerá un mensaje de bienvenida.

### 2. Enviar mensajes
1. Escribe tu mensaje en el campo de entrada.
2. Presiona la tecla **Enter** o haz clic en el botón **Enviar**.
3. El chatbot responderá de inmediato.

### 3. Guardar conversaciones
1. Tras interactuar con el chatbot, haz clic en el botón **Guardar Conversación**.
2. La conversación se almacenará en el archivo `conversations.json`.

### 4. Cargar conversaciones
1. Las conversaciones guardadas aparecen en la lista del sidebar.
2. Haz doble clic en una conversación para cargarla.

### 5. Eliminar conversaciones
1. Selecciona una conversación de la lista.
2. Haz clic en el botón **Borrar Conversación**.
3. La conversación se eliminará del archivo `conversations.json`.

### 6. Instrucciones adicionales
Haz clic en el botón **Instrucciones** para ver una guía rápida dentro de la aplicación.

## Temas de Conversación

- **Tecnología**: Consultas sobre últimos avances y tendencias.
- **Programación**: Teoría, mejores prácticas, y frameworks populares.
- **Ejemplos de código**:
  - Lenguaje **JavaScript**: Manipulación de DOM, funciones, promesas, etc.
  - Lenguaje **Python**: Operaciones con listas, manejo de archivos, etc.
- **Conversaciones casuales**: Ejercicios, estaciones del año y otros temas ligeros.

## Personalización
- La interfaz permite ajustar el tamaño de la ventana para mejorar la experiencia de usuario.
- Los colores y fuentes han sido elegidos para un entorno amigable y claro.

## Solución de Problemas

### Problema: No se guarda la conversación
1. Asegúrate de que el archivo `conversations.json` esté accesible y no esté dañado.
2. Verifica los permisos de escritura en el directorio.

### Problema: No se carga la imagen de la mascota
1. Confirma que el archivo `mascota.png` está en el directorio correcto.
2. Verifica la extensión y el nombre del archivo.

### Problema: La interfaz no responde
1. Cierra la aplicación y reiníciala.
2. Asegúrate de que todas las librerías estén instaladas correctamente.

## Actualizaciones Futuras
- Integración con bases de datos externas.
- Respuestas más personalizadas y con IA avanzada.
- Soporte multilenguaje.

## Contacto y Soporte
Para consultas técnicas o sugerencias, contáctanos en: **soporte@chatbot-ia1.com**.
