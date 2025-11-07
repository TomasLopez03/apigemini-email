import os
from dotenv import load_dotenv
from google import genai

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Obtiene la API key desde las variables de entorno
clave = os.getenv("GEMINI_API_KEY")

# Crea el cliente de GenAI con la API key
client = genai.Client(api_key=clave)