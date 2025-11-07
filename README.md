# 📧 Python Email & Gemini Content Generator

Este es un script simple de Python que demuestra cómo enviar correos electrónicos de manera segura usando el protocolo **SMTP** de Gmail, a la vez que utiliza la **API de Gemini** para generar contenido dinámico o borradores para el cuerpo del mensaje.

---

## 🛠️ Requisitos

Antes de empezar, asegúrate de tener instalado Python 3.x y lo siguiente:

1.  **Activación de la API:** Una clave válida para la [API de Gemini](https://ai.google.dev/).
2.  **Autenticación de Gmail (CRUCIAL):** Debes tener la **Verificación en dos pasos** activada en tu cuenta de Google y haber generado una **Contraseña de Aplicación** de 16 caracteres para usarla en lugar de tu contraseña principal.

## 🚀 Cómo Probarlo

Sigue estos sencillos pasos para poner en marcha el script.

### 1. Configuración Inicial

1.  **Clonar el Repositorio:**
    ```bash
    git clone https://github.com/TomasLopez03/apigemini-email.git
    cd apigemini-email
    ```

2.  **Crear el Entorno Virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    .\venv\Scripts\activate   # En Windows
    ```

3.  **Instalar Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

### 2. Configuración de Credenciales

Para mantener tus secretos a salvo de GitHub, usamos un archivo de entorno:

1.  **Copia la plantilla:**
    ```bash
    cp .env.example .env
    ```

2.  **Edita el archivo `.env`:** Abre el nuevo archivo `.env` y rellena las variables con tus credenciales reales:

    | Variable | Descripción | Valor de Ejemplo |
    | :--- | :--- | :--- |
    | `GEMINI_API_KEY` | Tu clave de la API de Gemini. | `AIzaSy...` |
    | `SENDER_EMAIL` | Tu dirección de Gmail. | `tu_correo@gmail.com` |
    | `GMAIL_APP_PASSWORD` | La **Contraseña de Aplicación** de 16 caracteres. | `abcd fghi jklm nopq` |
    | `RECEIVER_EMAIL` | El destinatario de prueba. | `prueba@ejemplo.com` |

### 3. Ejecutar el Script

Una vez que el archivo `.env` esté listo, simplemente ejecuta el script principal:

```bash
python app.py
```