import os # manejo de variables de entorno
import smtplib # envío de correos
from google.genai import types # tipos de la API de GenAI
from dotenv import load_dotenv # carga de variables de entorno
from email.message import EmailMessage # construcción de correos
from pydantic import BaseModel, Field # modelo de datos
from typing import List, Optional
from connection import client # Conexión a la API de GenAI

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Definición del modelo de datos esperado
class Client(BaseModel):
    name: str = Field(description="Name of the client")
    last_name: str = Field(description="Last name of the client")
    email: str = Field(description="Email of the client")
    amount_pending: Optional[float] = Field(description="Amount to pay if the client not paid the total yet")
    date_limit: str = Field(description="date limit to pay the fees")
    content: str = Field(description="Content of the email")
    subject: str = Field(description="Subject of the email")

class ListClient(BaseModel):
    clients: List[Client]

# Obtiene las direcciones de correo desde las variables de entorno
email_from = os.getenv("EMAIL_ADDRESS_FROM")
email_to = os.getenv("EMAIL_ADDRESS_TO")


personas = [
    {
        "name": "Tomas",
        "last_name": "Lopez",
        "email": email_to,
        "total_amount": 1500.0,
        "pay_amount": 0,
        "status": "pending",
        "date_create": "2025-11-07",
        "date_limit" : "2025-12-07"
    },
    {
        "name": "Gaston",
        "last_name": "Lopez",
        "email": email_to,
        "total_amount": 1500.0,
        "pay_amount": 1000.0,
        "status": "pending",
        "date_create": "2025-10-15",
        "date_limit" : "2025-11-15"
    },
    {
        "name": "Pedro",
        "last_name": "Lopez",
        "email": email_to,
        "total_amount": 1500.0,
        "pay_amount": 0,
        "status": "pending",
        "date_create": "2025-10-05",
        "date_limit" : "2025-11-05"
    },
]


# Genera el prompt para crear el contenido del email 
prompt = f"""
    From this List: {personas} analyze the data of every client, especially
    the create and limit date.
    Based on the difference between the creation date and deadline, create 
    the email content for each client. The subject could be ['creation notice',
    'near deadline', 'expiration'].
    Write an email in spanish to (take name and last name for each client),
    notifying them they situation, if the subejct is 'near deadline'/'expiration'
    calculate the pending amount(total amount - pay amount) 
    else pending amount = total amount.
    payment method ['transfencia bancaria', 'cheque', 'efectivo'].
    The email should be professional, polite.
    Name the sender as 'Estudio Geria Reines'.
    Make a name, position and contact information fictional from the sender.
    Not include that it's a draft note. 
    Always keep a justify content.
    *** IMPORTANT: Format the email content using HTML tags: 
    use <p> for paragraphs and <br> for line breaks. 
    Do not include <html> or <body> tags. ***
"""

# Llama a la API de GenAI para extraer los datos
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        system_instruction="You are a helpful assistant that writes professional emails.",
        response_mime_type="application/json",
        response_schema=ListClient.model_json_schema()
    )
)

# Valida y parsea la respuesta en el modelo de datos
clients = ListClient.model_validate_json(response.text)

# Campos del correo electrónico
msg= EmailMessage()

for cl in clients.clients:
    msg['Subject'] = cl.subject
    msg['From'] = email_from
    msg['To'] = cl.email
    # html para formato porfesional
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif;">
        {cl.content}
    </body>
    </html>
    """

    msg.add_alternative(html_content, subtype='html')

    # Envía el correo electrónico
    password_email = os.getenv("PASSWORD_EMAIL")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_from, password_email)
        smtp.send_message(msg)

    msg.clear()
