from dataclasses import dataclass, field
from typing import Dict, Optional

# tests for REQ1: register_patient(name, age)
req1_test = [
    {"name": "Anthony Soprano", "age": 21, "expected": True},
    {"name": "Jennifer Melfi", "age": 44, "expected": True},
    {"name": "Arthur Bucco", "age": 47, "expected": True},
]
# tests for REQ2: enter_person_into_and_symptoms(patient_id, symptoms)
req2_test = [
    {"patient_id": 1, "symptoms": "Headaches"},
    {"patient_id": 2, "symptoms": "Nausea\nHeartburn\nIndigestion"},
    {"patient_id": 3, "symptoms": "Dizziness\nShortness of breath"},
]

# tests for REQ3: move_patient_room(patient_id, new_room)
req3_test = [
    {"patient_id": 1, "new_room": "101"},
    {"patient_id": 2, "new_room": "207"},
    {"patient_id": 3, "new_room": "425"}
]




@dataclass
class Patient:
    patient_id: int
    name: str
    age: int
    symptoms: str
    current_room: Optional[str] = None


class HospitalSystem:
    def __init__(self):
        # Simple in‑memory "database" of patients
        self.patients: Dict[int, Patient] = {}
        self._next_id: int = 1

    # REQ1: Register patient in the system
    def register_patient(self, name: str, age: int) -> Patient:
        patient = Patient(
            patient_id=self._next_id,
            name=name,
            age=age,
            symptoms="",       # will be filled in REQ2
            current_room=None  # will be set in REQ3
        )
        self.patients[self._next_id] = patient
        self._next_id += 1
        print(f"[REQ1] Registered patient {patient.name} with ID {patient.patient_id}")
        return patient

    # REQ2: Patient enters personal information and symptoms
    # (basic personal info already captured; here we focus on symptoms update)
    def enter_personal_info_and_symptoms(self, patient_id: int, symptoms: str) -> None:
        patient = self.patients.get(patient_id)
        if not patient:
            raise ValueError("Patient not found")

        patient.symptoms = symptoms
        print(f"[REQ2] Updated symptoms for patient {patient.patient_id}: {patient.symptoms}")

    # REQ3: Patient moves rooms
    def move_patient_room(self, patient_id: int, new_room: str) -> None:
        patient = self.patients.get(patient_id)
        if not patient:
            raise ValueError("Patient not found")

        old_room = patient.current_room
        patient.current_room = new_room
        print(f"[REQ3] Patient {patient.patient_id} moved from {old_room} to {new_room}")


# REQ1 test
def req1test(system: HospitalSystem):
    for case in req1_test:
        patient = system.register_patient(case["name"], case["age"])
        assert isinstance(patient, Patient), f"Failed REQ1: {case}"

# REQ2 test
def req2test(system: HospitalSystem):
    for case in req2_test:
        system.enter_personal_info_and_symptoms(case["patient_id"], case["symptoms"])
        patient = system.patients[case["patient_id"]]
        assert patient.symptoms == case["symptoms"], f"Failed REQ2: {case}"

# REQ3 test
def req3test(system: HospitalSystem):
    for case in req3_test:
        system.move_patient_room(case["patient_id"], case["new_room"])
        patient = system.patients[case["patient_id"]]
        assert patient.current_room == case["new_room"], f"Failed REQ3: {case}"



# Example for testing purposes

if __name__ == "__main__":
    system = HospitalSystem()

    # TESTING BLOCK
    req1test(system)
    
    req2test(system)
    
    req3test(system)

    # REQ1: Register patient
    p = system.register_patient(name="John Doe", age=45)

    # REQ2: Enter symptoms
    system.enter_personal_info_and_symptoms(
        patient_id=p.patient_id,
        symptoms="Fever, cough, shortness of breath"
    )

    # REQ3: Move rooms
    system.move_patient_room(
        patient_id=p.patient_id,
        new_room="Room 203B"
    )

    # Quick check of stored state
    print("\nFinal patient record:")
    print(system.patients[p.patient_id])