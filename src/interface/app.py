import streamlit as st
import json
from groq import Groq
from datetime import datetime
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.core.hospital_coordinator import HospitalCoordinator
from src.config.settings import GROQ_API_KEY

def initialize_session_state():
    """Initialize session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_case' not in st.session_state:
        st.session_state.current_case = None
    if 'coordinator' not in st.session_state:
        client = Groq(api_key=GROQ_API_KEY)
        st.session_state.coordinator = HospitalCoordinator(client)

def display_header():
    """Display the application header"""
    st.title("🏥 Sistema de Asistencia Hospitalaria Virtual")
    st.markdown("""
    Bienvenido al Sistema de Asistencia Hospitalaria Virtual. 
    Por favor, describa sus síntomas o el motivo de su consulta.
    """)

def display_chat_history():
    """Display the chat history"""
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant" and isinstance(message["content"], dict):
                display_medical_response(message["content"])
            else:
                st.write(message["content"])

def display_medical_response(response):
    """Display the medical response in a structured format"""
    if "error" in response:
        st.error(f"Error: {response['error']}")
        if "details" in response:
            st.error(f"Detalles: {response['details']}")
        return

    try:
        # Display urgency level with appropriate color
        urgency_level = response.get("triage_evaluation", {}).get("urgency_level", 5)
        urgency_color = {
            1: "🔴 EMERGENCIA",
            2: "🟠 MUY URGENTE",
            3: "🟡 URGENTE",
            4: "🟢 NORMAL",
            5: "🔵 NO URGENTE"
        }.get(urgency_level, "⚪ NO ESPECIFICADO")

        st.markdown(f"### Estado: {urgency_color}")

        # Create tabs for different sections
        tabs = st.tabs([
            "Evaluación Inicial", 
            "Plan de Acción", 
            "Especialista", 
            "Farmacia",
            "Enfermería"
        ])

        # Triage Evaluation
        with tabs[0]:
            triage = response.get("triage_evaluation", {})
            st.markdown("#### Evaluación de Triaje")
            st.write(f"**Departamento:** {triage.get('department', 'No especificado')}")
            st.write("**Acciones Inmediatas:**")
            for action in triage.get('immediate_actions', []):
                st.write(f"- {action}")
            st.write(f"**Razonamiento:** {triage.get('reasoning', 'No especificado')}")

        # Action Plan
        with tabs[1]:
            st.markdown("#### Próximos Pasos")
            for step in response.get('next_steps', []):
                st.write(f"- {step}")
            if response.get('follow_up'):
                st.write(f"**Seguimiento:** {response['follow_up']}")

        # Specialist Evaluation
        with tabs[2]:
            if spec_eval := response.get('specialist_evaluation'):
                st.markdown("#### Evaluación del Especialista")
                st.write(f"**Diagnóstico:** {spec_eval.get('diagnosis', 'No especificado')}")
                st.write(f"**Nivel de Confianza:** {spec_eval.get('confidence_level', 0)}%")
                
                st.write("**Pruebas Requeridas:**")
                for test in spec_eval.get('required_tests', []):
                    st.write(f"- {test}")
                
                st.write("**Plan de Tratamiento:**")
                for step in spec_eval.get('treatment_plan', []):
                    st.write(f"- {step}")

        # Pharmacy Review
        with tabs[3]:
            if pharmacy := response.get('pharmacy_review', {}):
                st.markdown("#### Revisión Farmacéutica")
                for prescription in pharmacy.get('prescripciones', []):
                    med_name = prescription.get('medicamento', 'No especificado')
                    st.write(f"**{med_name}**")
                    if 'dosis' in prescription:
                        st.write(f"- Dosis: {prescription['dosis']}")
                    if 'frecuencia' in prescription:
                        st.write(f"- Frecuencia: {prescription['frecuencia']}")
                    if 'indicacion' in prescription:
                        st.write(f"- Indicación: {prescription['indicacion']}")

        # Nursing Care
        with tabs[4]:
            if nursing := response.get('nursing_care', {}):
                st.markdown("#### Cuidados de Enfermería")
                if eval_inicial := nursing.get('evaluacion_inicial', {}):
                    st.write("**Evaluación Inicial:**")
                    st.write(f"- Prioridad: {eval_inicial.get('prioridad', 'No especificada')}")
                    st.write(f"- Diagnóstico Posible: {eval_inicial.get('posible_diagnostico', 'No especificado')}")

    except Exception as e:
        st.error(f"Error al mostrar la respuesta: {str(e)}")

def main():
    initialize_session_state()
    display_header()

    # Display chat history
    display_chat_history()

    # Get user input
    if prompt := st.chat_input("Describa sus síntomas..."):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        try:
            # Process the case
            result = st.session_state.coordinator.process_case(prompt)

            # Add assistant response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": result})

            # Rerun to update the display
            st.rerun()
        except Exception as e:
            st.error(f"Error al procesar el caso: {str(e)}")

if __name__ == "__main__":
    main() 