from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API Configuration
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
MODEL_NAME = "llama-3.3-70b-versatile"

# Agent Configuration
TEMPERATURE = 0.2
MAX_TOKENS = 1024

# Hospital Configuration
URGENCY_LEVELS = {
    1: "Resucitación (atención inmediata)",
    2: "Emergencia (muy urgente, minutos)",
    3: "Urgente (hasta 1 hora)",
    4: "Menos urgente (hasta 2 horas)",
    5: "No urgente (hasta 4 horas)"
}

# Response Format Configuration
RESPONSE_FORMAT = {"type": "json_object"} 