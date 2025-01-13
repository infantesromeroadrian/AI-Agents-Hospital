from typing import Dict
from src.core.base_agent import BaseAgent

class SpecialistAgent(BaseAgent):
    def _get_system_prompt(self) -> str:
        return """Eres un médico especialista experto. Tu tarea es proporcionar una evaluación médica detallada.

DEBES responder ÚNICAMENTE con un JSON válido que siga esta estructura exacta:
{
    "diagnosis": string,              // Diagnóstico preliminar basado en síntomas
    "confidence_level": int,          // Nivel de confianza (1-100)
    "required_tests": [string],       // Lista de pruebas necesarias
    "treatment_plan": [string],       // Plan de tratamiento paso a paso
    "prescriptions": [string],        // Medicamentos recetados con dosis
    "follow_up": string,              // Tiempo para siguiente revisión
    "warnings": [string],             // Advertencias y precauciones
    "specialist_notes": string        // Observaciones importantes
}

Consideraciones importantes:
1. Diagnóstico: Ser específico y basado en evidencia
2. Pruebas: Ordenar de más a menos urgente
3. Tratamiento: Incluir medidas inmediatas y a largo plazo
4. Medicamentos: Especificar dosis y frecuencia
5. Advertencias: Incluir contraindicaciones y efectos secundarios"""

    def evaluate_case(self, patient_data: str, specialty: str) -> Dict:
        prompt = f"""Como especialista en {specialty}, por favor evalúa el siguiente caso clínico:

Datos del paciente: {patient_data}

Proporciona:
1. Un diagnóstico preliminar detallado
2. Las pruebas médicas necesarias
3. Un plan de tratamiento completo
4. Las prescripciones médicas requeridas
5. Recomendaciones de seguimiento
6. Advertencias relevantes

Asegúrate de que tu respuesta siga EXACTAMENTE el formato JSON especificado."""
        
        return self._make_llm_call(prompt) 