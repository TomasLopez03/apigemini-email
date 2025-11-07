import os # manejo de variables de entorno
import smtplib # envío de correos
from google.genai import types # tipos de la API de GenAI
from dotenv import load_dotenv # carga de variables de entorno
from email.message import EmailMessage # construcción de correos
from pydantic import BaseModel # modelo de datos
from connection import client # Conexión a la API de GenAI

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Definición del modelo de datos esperado
class Data(BaseModel):
    name: str
    last_name: str
    email: str
    amount_pending: float 

# Obtiene las direcciones de correo desde las variables de entorno
email_from = os.getenv("EMAIL_ADDRESS_FROM")
email_to = os.getenv("EMAIL_ADDRESS_TO")


personas = [
    {
        "name": "Tomas",
        "last_name": "Lopez",
        "email": email_to,
        "total_amount": 1500.0,
        "pay_amount": 500.0,
        "status": "pending"
    },
]

# Genera el prompt para extraer los datos necesarios 
prompt = f"""
    Please extract the data from the following list of people,
    i need the following fields: name, last_name, email, amount_pending.
    amount_pending is the total_amount minus the pay_amount.
    List of people: {personas}
"""

# Llama a la API de GenAI para extraer los datos
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_schema": Data.model_json_schema()
    }
)

# Valida y parsea la respuesta en el modelo de datos
data = Data.model_validate_json(response.text)

# Genera el prompt para el correo electrónico
prompt = f"""
    Write an email in spanish to {data.name} {data.last_name}, notifying them
    that they have an outstanding amount of ${data.amount_pending:.2f}.
    The email should be professional and polite and human.
    Name the sender as "Estudio Contable Falso".
    The amount is from previous services provided. the date of the services
    was one month ago.
    Make a name, position and contact information fictional from the sender.
    Not include that it's a draft note.
"""
# Llama a la API de GenAI para generar el cuerpo del correo
response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a helpful assistant that writes professional emails."
    ),
    contents=prompt
)

cuerpo = response.text

# Campos del correo electrónico
msg= EmailMessage()
msg['Subject'] = 'Notificación de pago pendiente'
msg['From'] = email_from
msg['To'] = data.email
msg.set_content(cuerpo)

# Envía el correo electrónico
password_email = os.getenv("PASSWORD_EMAIL")
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_from, password_email)
    smtp.send_message(msg)