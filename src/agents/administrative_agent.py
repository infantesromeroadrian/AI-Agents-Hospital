from typing import Dict
from src.core.base_agent import BaseAgent

class AdministrativeAgent(BaseAgent):
    def _get_system_prompt(self) -> str:
        return """Eres un administrador hospitalario experto. Tu tarea es gestionar admisiones y recursos hospitalarios.

DEBES responder UNICAMENTE con un JSON valido que siga esta estructura exacta:
{
    "admission_details": {
        "room_assignment": string,    // Ejemplo: "Room 101"
        "bed_type": string,          // Ejemplo: "Standard"
        "ward": string,              // Ejemplo: "General"
        "estimated_stay": string     // Ejemplo: "2 days"
    },
    "resource_requirements": [
        {
            "resource": string,      // Nombre del recurso
            "priority": int,         // Numero del 1 al 5
            "quantity": int          // Cantidad como numero entero
        }
    ],
    "staff_assignments": [
        {
            "role": string,         // Ejemplo: "Nurse"
            "shift": string,        // Ejemplo: "Morning"
            "special_notes": string // Notas sin caracteres especiales
        }
    ],
    "cost_estimate": {
        "daily_rate": float,        // Ejemplo: 500.00
        "special_services": float,  // Ejemplo: 150.00
        "estimated_total": float    // Ejemplo: 1000.00 (valor fijo)
    },
    "special_requirements": [string],
    "administrative_notes": string,
    "follow_up_actions": [string]
}

IMPORTANTE:
- NO uses caracteres especiales ni acentos
- NO hagas calculos matematicos
- Usa valores fijos para todos los numeros
- Para estimated_total usa un valor fijo, no lo calcules"""

    def manage_admission(self, patient_id: str, medical_data: Dict, insurance_info: str = None) -> Dict:
        prompt = f"""Por favor, gestiona la admision del siguiente paciente:

ID Paciente: {patient_id}
Datos medicos: {medical_data}
Informacion de seguro: {insurance_info if insurance_info else 'No disponible'}

Proporciona:
1. Detalles completos de la admision
2. Requerimientos de recursos
3. Asignacion de personal
4. Estimacion de costos (usa valores fijos)
5. Requisitos especiales
6. Plan de seguimiento administrativo

IMPORTANTE:
- NO uses caracteres especiales ni acentos
- NO hagas calculos matematicos
- Usa valores fijos para todos los numeros
- Para estimated_total usa un valor fijo, no lo calcules
- Evita usar apostrofes (') en el texto

Asegurate de que tu respuesta siga EXACTAMENTE el formato JSON especificado."""
        
        return self._make_llm_call(prompt) 