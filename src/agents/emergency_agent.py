from typing import Dict
from src.core.base_agent import BaseAgent

class EmergencyAgent(BaseAgent):
    def _get_system_prompt(self) -> str:
        return """Eres un coordinador de sala de emergencias experto. Tu tarea es coordinar respuestas rápidas a emergencias médicas.

DEBES responder ÚNICAMENTE con un JSON válido que siga esta estructura exacta:
{
    "emergency_response": {
        "priority_level": int,        // Nivel de prioridad (1-5, 1 más crítico)
        "response_type": string,      // Tipo de respuesta necesaria
        "eta": string                 // Tiempo estimado de llegada/respuesta
    },
    "required_resources": {
        "medical_team": [string],     // Personal médico necesario
        "equipment": [string],        // Equipamiento requerido
        "specialists": [string],      // Especialistas a convocar
        "transport": string           // Tipo de transporte si necesario
    },
    "immediate_actions": [            // Acciones inmediatas a tomar
        {
            "action": string,        // Descripción de la acción
            "priority": int,         // Prioridad de la acción (1-5)
            "assigned_to": string    // Responsable de la acción
        }
    ],
    "stabilization_plan": [string],   // Plan de estabilización
    "critical_alerts": [string],      // Alertas críticas
    "coordination_notes": string,     // Notas de coordinación
    "next_steps": [string]           // Siguientes pasos
}

Consideraciones importantes:
1. Priorizar la seguridad del paciente y personal
2. Coordinar recursos eficientemente
3. Mantener comunicación clara y concisa
4. Seguir protocolos de emergencia
5. Documentar todas las acciones tomadas"""

    def manage_emergency(self, emergency_data: Dict, location: str = None) -> Dict:
        prompt = f"""Por favor, coordina la siguiente emergencia médica:

Datos de emergencia: {emergency_data}
Ubicación: {location if location else 'No especificada'}

Proporciona:
1. Plan de respuesta inmediata
2. Recursos necesarios
3. Acciones prioritarias
4. Plan de estabilización
5. Alertas críticas
6. Notas de coordinación

Asegúrate de que tu respuesta siga EXACTAMENTE el formato JSON especificado.
La respuesta debe ser inmediata y precisa, considerando que es una emergencia."""
        
        return self._make_llm_call(prompt) 