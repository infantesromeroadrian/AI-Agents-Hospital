from typing import Dict
from src.core.base_agent import BaseAgent

class NurseAgent(BaseAgent):
    def _get_system_prompt(self) -> str:
        return """Eres un enfermero/a experto/a. Tu tarea es monitorear al paciente y establecer un plan de cuidados.

DEBES responder ÚNICAMENTE con un JSON válido que siga esta estructura exacta:
{
    "vital_signs_status": {           // Estado actual de signos vitales
        "temperature": string,        // Temperatura
        "blood_pressure": string,     // Presión arterial
        "heart_rate": string,         // Frecuencia cardíaca
        "oxygen_saturation": string   // Saturación de oxígeno
    },
    "care_tasks": [string],          // Lista de tareas de cuidado necesarias
    "monitoring_frequency": string,   // Frecuencia de monitoreo requerida
    "alert_conditions": [string],     // Condiciones que requieren atención inmediata
    "comfort_measures": [string],     // Medidas para el confort del paciente
    "nursing_notes": string,          // Observaciones importantes de enfermería
    "next_evaluation": string         // Cuándo realizar la siguiente evaluación
}

Consideraciones importantes:
1. Priorizar la seguridad del paciente
2. Mantener un monitoreo constante de signos vitales
3. Documentar cualquier cambio significativo
4. Asegurar el cumplimiento del plan de tratamiento
5. Mantener la comodidad del paciente"""

    def monitor_patient(self, patient_id: str, patient_data: str, care_plan: Dict) -> Dict:
        prompt = f"""Por favor, evalúa y monitorea al siguiente paciente:

ID Paciente: {patient_id}
Datos del paciente: {patient_data}
Plan de cuidados actual: {care_plan}

Proporciona:
1. Estado actual de signos vitales
2. Lista de tareas de cuidado necesarias
3. Frecuencia de monitoreo requerida
4. Condiciones que requieren atención inmediata
5. Medidas para el confort del paciente
6. Observaciones de enfermería relevantes

Asegúrate de que tu respuesta siga EXACTAMENTE el formato JSON especificado."""
        
        return self._make_llm_call(prompt) 