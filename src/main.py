from groq import Groq
from config.settings import GROQ_API_KEY
from core.hospital_coordinator import HospitalCoordinator
import json

def main():
    try:
        # Initialize Groq client
        client = Groq(api_key=GROQ_API_KEY)
        
        # Initialize hospital coordinator
        coordinator = HospitalCoordinator(client)
        
        # Example case
        test_case = """
        Paciente de 58 años presenta:
        - Dolor intenso en el pecho que irradia al brazo izquierdo
        - Sudoración fría
        - Dificultad para respirar
        - Náuseas
        - Antecedentes de hipertensión y diabetes
        - Fumador activo
        Tiempo de evolución: 30 minutos
        """
        
        # Process the case
        result = coordinator.process_case(
            test_case,
            location="Calle Principal 123, Apartamento 4B"
        )
        
        if result is None:
            print("Error: No se recibió respuesta del sistema")
            return
        
        # Print results
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"Error en la ejecución: {str(e)}")

if __name__ == "__main__":
    main() 