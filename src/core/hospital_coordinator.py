from typing import Dict
from datetime import datetime
import logging
from src.agents.triage_agent import TriageAgent
from src.agents.specialist_agent import SpecialistAgent
from src.agents.nurse_agent import NurseAgent
from src.agents.pharmacist_agent import PharmacistAgent
from src.agents.administrative_agent import AdministrativeAgent
from src.agents.emergency_agent import EmergencyAgent

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HospitalCoordinator:
    """Coordinates all hospital agents and manages patient cases"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        try:
            self.triage_agent = TriageAgent(api_key)
            self.specialist_agent = SpecialistAgent(api_key)
            self.nurse_agent = NurseAgent(api_key)
            self.pharmacist_agent = PharmacistAgent(api_key)
            self.administrative_agent = AdministrativeAgent(api_key)
            self.emergency_agent = EmergencyAgent(api_key)
            logger.info("Hospital Coordinator initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Hospital Coordinator: {str(e)}")
            raise
    
    def process_case(self, patient_data: str, location: str = None) -> Dict:
        """Process a complete hospital case using all agents"""
        patient_id = f"P{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        try:
            logger.info(f"Starting case processing for patient: {patient_id}")
            
            # 1. Initial triage
            logger.info("Initiating triage evaluation")
            triage_result = self.triage_agent.evaluate_patient(patient_data)
            if "error" in triage_result:
                logger.error(f"Triage evaluation failed: {triage_result['error']}")
                return self._create_error_response("Triage evaluation failed", triage_result['error'])
            
            urgency_level = triage_result.get("urgency_level", 5)
            logger.info(f"Triage completed. Urgency level: {urgency_level}")
            
            # 2. Emergency protocol for level 1
            emergency_response = None
            if urgency_level == 1:
                logger.info("Activating emergency protocol")
                emergency_data = {
                    "case_id": patient_id,
                    "patient_condition": {
                        "main_symptom": patient_data,
                        "triage_assessment": triage_result
                    }
                }
                emergency_response = self.emergency_agent.manage_emergency(emergency_data, location)
                if "error" in emergency_response:
                    logger.error(f"Emergency response failed: {emergency_response['error']}")
                    return self._create_error_response("Emergency response failed", emergency_response['error'])
            
            # 3. Specialist evaluation
            logger.info("Starting specialist evaluation")
            department = triage_result.get("department", "Medicina General")
            specialist_evaluation = self.specialist_agent.evaluate_case(patient_data, department)
            if "error" in specialist_evaluation:
                logger.error(f"Specialist evaluation failed: {specialist_evaluation['error']}")
                return self._create_error_response("Specialist evaluation failed", specialist_evaluation['error'])
            
            # 4. Pharmacy review
            logger.info("Initiating pharmacy review")
            prescriptions = specialist_evaluation.get("prescriptions", [])
            pharmacy_review = self.pharmacist_agent.review_prescription(
                patient_id,
                prescriptions,
                patient_data
            )
            if "error" in pharmacy_review:
                logger.error(f"Pharmacy review failed: {pharmacy_review['error']}")
                return self._create_error_response("Pharmacy review failed", pharmacy_review['error'])
            
            # 5. Nursing care
            logger.info("Setting up nursing care plan")
            nursing_care = self.nurse_agent.monitor_patient(
                patient_id,
                patient_data,
                specialist_evaluation
            )
            if "error" in nursing_care:
                logger.error(f"Nursing care setup failed: {nursing_care['error']}")
                return self._create_error_response("Nursing care setup failed", nursing_care['error'])
            
            # 6. Administrative management
            logger.info("Processing administrative tasks")
            admin_data = {
                "diagnosis": specialist_evaluation.get("diagnosis"),
                "urgency_level": urgency_level,
                "special_needs": nursing_care.get("care_tasks", []),
                "estimated_stay": "1-2 días" if urgency_level > 3 else "3-7 días"
            }
            
            admin_plan = self.administrative_agent.manage_admission(patient_id, admin_data)
            if "error" in admin_plan:
                logger.error(f"Administrative processing failed: {admin_plan['error']}")
                return self._create_error_response("Administrative processing failed", admin_plan['error'])
            
            # 7. Prepare complete response
            logger.info("Finalizing case processing")
            return {
                "case_id": patient_id,
                "status": "EMERGENCY" if urgency_level == 1 else "URGENT" if urgency_level <= 3 else "REGULAR",
                "triage_evaluation": triage_result,
                "emergency_response": emergency_response,
                "specialist_evaluation": specialist_evaluation,
                "pharmacy_review": pharmacy_review,
                "nursing_care": nursing_care,
                "administrative_plan": admin_plan,
                "next_steps": triage_result.get("immediate_actions", []),
                "follow_up": specialist_evaluation.get("follow_up"),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing case: {str(e)}", exc_info=True)
            return self._create_error_response("Error processing case", str(e))
    
    def _create_error_response(self, error_type: str, details: str) -> Dict:
        """Create a standardized error response"""
        return {
            "error": error_type,
            "details": details,
            "timestamp": datetime.now().isoformat()
        } 