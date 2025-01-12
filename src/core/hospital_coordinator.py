from typing import Dict
from datetime import datetime
from src.agents.triage_agent import TriageAgent
from src.agents.specialist_agent import SpecialistAgent
from src.agents.nurse_agent import NurseAgent
from src.agents.pharmacist_agent import PharmacistAgent
from src.agents.administrative_agent import AdministrativeAgent
from src.agents.emergency_agent import EmergencyAgent

class HospitalCoordinator:
    """Coordinates all hospital agents and manages patient cases"""
    
    def __init__(self, client):
        self.triage_agent = TriageAgent(client)
        self.specialist_agent = SpecialistAgent(client)
        self.nurse_agent = NurseAgent(client)
        self.pharmacist_agent = PharmacistAgent(client)
        self.admin_agent = AdministrativeAgent(client)
        self.emergency_agent = EmergencyAgent(client)
    
    def process_case(self, patient_data: str, location: str = None) -> Dict:
        """Process a complete hospital case using all agents"""
        patient_id = f"P{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        try:
            # 1. Initial triage
            triage_result = self.triage_agent.evaluate_patient(patient_data)
            urgency_level = triage_result.get("urgency_level", 5)
            
            # 2. If very urgent (level 1), activate emergency protocol
            if urgency_level == 1:
                emergency_data = {
                    "case_id": patient_id,
                    "patient_condition": {
                        "main_symptom": patient_data,
                        "triage_assessment": triage_result
                    }
                }
                emergency_response = self.emergency_agent.manage_emergency(emergency_data, location)
            else:
                emergency_response = None
            
            # 3. Specialist evaluation
            department = triage_result.get("department", "Medicina General")
            specialist_evaluation = self.specialist_agent.evaluate_case(patient_data, department)
            
            # 4. Pharmacy review
            prescriptions = specialist_evaluation.get("prescriptions", [])
            pharmacy_review = self.pharmacist_agent.review_prescription(
                patient_id,
                prescriptions,
                patient_data
            )
            
            # 5. Nursing care
            nursing_care = self.nurse_agent.monitor_patient(
                patient_id,
                patient_data,
                specialist_evaluation
            )
            
            # 6. Administrative management
            admin_data = {
                "diagnosis": specialist_evaluation.get("diagnosis"),
                "urgency_level": urgency_level,
                "special_needs": nursing_care.get("care_tasks", []),
                "estimated_stay": "1-2 días" if urgency_level > 3 else "3-7 días"
            }
            
            admin_plan = self.admin_agent.manage_admission(patient_id, admin_data)
            
            # 7. Prepare complete response
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
            return {
                "error": "Error processing case",
                "details": str(e),
                "timestamp": datetime.now().isoformat()
            } 