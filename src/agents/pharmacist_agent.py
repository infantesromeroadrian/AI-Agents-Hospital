from typing import Dict, List
from src.core.base_agent import BaseAgent

class PharmacistAgent(BaseAgent):
    def _get_system_prompt(self) -> str:
        return """Eres un farmacéutico experto. Tu tarea es revisar prescripciones y asegurar la seguridad del paciente.

DEBES responder ÚNICAMENTE con un JSON válido que siga esta estructura exacta:
{
    "prescription_review": [          // Análisis de cada medicamento
        {
            "medication": string,     // Nombre del medicamento
            "dosage_check": string,   // Evaluación de la dosis
            "interactions": [string], // Posibles interacciones
            "side_effects": [string], // Efectos secundarios principales
            "recommendations": string // Recomendaciones específicas
        }
    ],
    "safety_alerts": [string],       // Alertas de seguridad importantes
    "substitutions": [               // Sustituciones sugeridas
        {
            "original": string,      // Medicamento original
            "suggested": string,     // Sustituto sugerido
            "reason": string        // Razón del cambio
        }
    ],
    "administration_notes": string,  // Notas sobre la administración
    "patient_instructions": [string], // Instrucciones para el paciente
    "monitoring_required": [string]  // Parámetros a monitorear
}

Consideraciones importantes:
1. Verificar dosis y frecuencia de administración
2. Identificar posibles interacciones medicamentosas
3. Evaluar contraindicaciones basadas en el historial del paciente
4. Sugerir alternativas más seguras o económicas cuando sea apropiado
5. Proporcionar instrucciones claras para el paciente"""

    def review_prescription(self, patient_id: str, prescriptions: List[str], patient_data: str) -> Dict:
        prompt = f"""Por favor, realiza una revisión farmacéutica completa:

ID Paciente: {patient_id}
Datos del paciente: {patient_data}
Prescripciones a revisar: {prescriptions}

Proporciona:
1. Análisis detallado de cada medicamento prescrito
2. Posibles interacciones medicamentosas
3. Efectos secundarios relevantes
4. Sustituciones recomendadas si aplica
5. Instrucciones específicas para el paciente
6. Requisitos de monitoreo

Asegúrate de que tu respuesta siga EXACTAMENTE el formato JSON especificado."""
        
        return self._make_llm_call(prompt) 