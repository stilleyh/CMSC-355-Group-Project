from dataclasses import dataclass, field
from typing import Dict, Optional, List
from flask import Flask, request, jsonify
import sqlite3
import json
import pdb

app = Flask(__name__, static_folder=".", static_url_path="")

# DATA MODELS
# PATIENTS
@dataclass
class Patient:
    patient_id: int
    name: str
    age: int
    symptoms: str = ""
    room: Optional[str] = None
    vitals: Dict[str, str] = field(default_factory=dict)
    diagnosis: Optional[str] = None
    specialist: Optional[str] = None
    medication: Optional[str] = None
    discharged: bool = False
    lab_results: Optional[str] = None
    notes: List[str] = field(default_factory=list)

# STAFF
@dataclass
class Staff:
    firstname: str
    lastname: str
    position: str
    email: str

# LOGINS
@dataclass
class Login:
    username: str
    password: str

# APPOINTMENTS
@dataclass
class Appointment:
    doctor: str
    room: str
    time: str
    procedure_reason: str
    urgent: bool = False
    notes: List[str] = field(default_factory=list)
    patient_id: int

@dataclass
class HospitalSystem:
    patients: Dict[int, Patient] = field(default_factory=dict)
    next_patient_id: int = 1

    # REQ1 – Register Patient
    def register_patient(self, name: str, age: int) -> bool:
        patient = Patient(self.next_patient_id, name, age)
        self.patients[self.next_patient_id] = patient
        self.next_patient_id += 1
#        pdb.set_trace() # DEBUG
        return patient.patient_id

    # REQ2 – Enter Personal Info + Symptoms
    def enter_person_info_and_symptoms(self, patient_id: int, symptoms: str) -> bool:
        if patient_id not in self.patients:
            return False
        self.patients[patient_id].symptoms = symptoms
        return True

    # REQ3 – Move Rooms
    def move_patient_room(self, patient_id: int, new_room: str) -> bool:
        if patient_id not in self.patients:
            return False
        self.patients[patient_id].room = new_room
        return True

    # REQ4 – Patient Answers Questions
    def patient_answers_questions(self, patient_id: int, answers: str):
        if patient_id not in self.patients:
            return False
        self.patients[patient_id].notes.append(f"Patient answers: {answers}")
        return True

    # REQ5 – Examination
    def perform_examination(self, patient_id: int, exam_notes: str):
        if patient_id not in self.patients:
            return False
        self.patients[patient_id].notes.append(f"Exam: {exam_notes}")
        return True


    # REQ6 – Lab Tests
    def perform_lab_test(self, patient_id: int, results: str):
        if patient_id not in self.patients:
            return False
        self.patients[patient_id].lab_results = results
        return True

    # REQ7 – Monitoring
    def monitor_patient(self, patient_id: int, note: str):
        if patient_id not in self.patients:
            return False
        self.patients[patient_id].notes.append(f"Monitoring: {note}")
        return True

    # REQ8 – Support
    def support_patient(self, patient_id: int, support_note: str):
        if patient_id not in self.patients:
            return False
        self.patients[patient_id].notes.append(f"Support: {support_note}")
        return True

    # REQ9 – Prescribe Medication
    def prescribe_medication(self, patient_id: int, medication: str):
        if patient_id not in self.patients:
            return False
        self.patients[patient_id].medication = medication
        return True

    # REQ10 – Discharge
    def discharge_patient(self, patient_id: int):
        if patient_id not in self.patients:
            return False
        self.patients[patient_id].discharged = True
        return True

    # DOCTOR REQS (11–18)
    def doctor_receive_info(self, patient_id: int):
        return self.patients.get(patient_id)

    def doctor_take_notes(self, patient_id: int, note: str):
        return self.monitor_patient(patient_id, f"Doctor note: {note}")

    def doctor_send_for_lab(self, patient_id: int):
        return True

    def doctor_check_lab(self, patient_id: int):
        return self.patients[patient_id].lab_results

    def doctor_make_diagnosis(self, patient_id: int, diagnosis: str):
        self.patients[patient_id].diagnosis = diagnosis
        return True

    def doctor_assign_specialist(self, patient_id: int, specialist: str):
        self.patients[patient_id].specialist = specialist
        return True

    def doctor_update_system(self, patient_id: int):
        return True

    # ADMIN REQS (19–36)
    def admin_create_profile(self, patient_id: int):
        return self.patients.get(patient_id)

    def admin_take_vitals(self, patient_id: int, vitals: Dict[str, str]):
        self.patients[patient_id].vitals = vitals
        return True

    def admin_send_info_to_doctor(self, patient_id: int):
        return self.patients.get(patient_id)

    def admin_receive_lab_request(self, patient_id: int):
        return True

    def admin_send_lab_results(self, patient_id: int):
        return self.patients[patient_id].lab_results

    def admin_send_prescription(self, patient_id: int):
        return self.patients[patient_id].medication

    def admin_log_all_info(self, patient_id: int):
        return self.patients[patient_id].__dict__

    def admin_discharge_patient(self, patient_id: int):
        return self.discharge_patient(patient_id)

    def admin_create_bill(self, patient_id: int):
        return f"Bill for patient {patient_id}: $500"

    def admin_send_bill(self, patient_id: int):
        return True

    def admin_manage_rooms(self):
        return True

    def admin_manage_medicine(self):
        return True

    def admin_manage_equipment(self):
        return True

    def admin_schedule_appointment(self):
        return True

    def admin_cancel_appointment(self):
        return True

# BOOT/LOAD STAFF DATABASE INTO MEMORY
# IF NO DATABASE EXISTS, CREATE NEW TABLE
def boot_and_load_staff() -> List[Staff]:
    conn = sqlite3.connect("hospital.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        firstname TEXT,
        lastname TEXT,
        position TEXT,
        email TEXT
    )
    """)

    cur.execute("SELECT * FROM staff")
    rows = cur.fetchall()

    staff_members = []

    for row in rows:
        staff_members.append(Staff(
            firstname=row["firstname"],
            lastname=row["lastname"],
            position=row["position"],
            email=row["email"]
        ))

    conn.close()
    return staff_members

# BOOT/LOAD APPOINTMENTS DATABASE
def boot_and_load_appointments() -> List[Appointment]:
    conn = sqlite3.connect("hospital.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        doctor TEXT,
        room TEXT,
        time TEXT,
        procedure_reason TEXT,
        urgent INTEGER,
        notes TEXT,
        patient_id INTEGER
    )
    """)

    cur.execute("SELECT * FROM appointments")
    rows = cur.fetchall()

    appointments = []

    for row in rows:
        appointments.append(Appointment(
            doctor=row["doctor"],
            room=row["room"],
            time=row["time"],
            procedure_reason=row["procedure_reason"],
            urgent=bool(row["urgent"]),
            notes=json.loads(row["notes"]) if row["notes"] else [],
            patient_id=row["patient_id"]
        ))

    conn.close()
    return appointments


# BOOT/LOAD PATIENT DATABASE INTO MEMORY
# IF NO DATABASE EXISTS, CREATE NEW TABLE
def boot_and_load_patients():
    conn = sqlite3.connect("patients.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        patient_id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        symptoms TEXT,
        room TEXT,
        vitals TEXT,
        diagnosis TEXT,
        specialist TEXT,
        medication TEXT,
        discharged INTEGER,
        lab_results TEXT,
        notes TEXT
    )
    """)

    cur.execute("SELECT * FROM patients")
    rows = cur.fetchall()

    patients = []

    for row in rows:
        patients.append(Patient(
            patient_id=int(row["patient_id"]),
            name=row["name"],
            age=row["age"],
            symptoms=row["symptoms"] or "",
            room=row["room"],
            vitals=json.loads(row["vitals"]) if row["vitals"] else {},
            diagnosis=row["diagnosis"],
            specialist=row["specialist"],
            medication=row["medication"],
            discharged=bool(row["discharged"]),
            lab_results=row["lab_results"],
            notes=json.loads(row["notes"]) if row["notes"] else []
        ))

    conn.close()
    
    return patients

# Load databases to memory
patients = boot_and_load_patients()
staff = boot_and_load_staff()
appointments = boot_and_load_appointments()

print("LOADED FROM DB: patients =", len(patients))
print("LOADED FROM DB: staff =", len(staff))
print("LOADED FROM DB: appointments =", len(appointments))

system = HospitalSystem(
    staff=staff,
    appointments=appointments,
    patients={p.patient_id: p for p in patients}
)

system.next_patient_id = max(system.patients, default=0) + 1

# SAVE PATIENT LIST TO DATABASE
# DELETES DATABASE CONTENT AND REPLACES WITH CURRENT TABLE
def save_patients_to_db(patients):
    conn = sqlite3.connect("patients.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM patients")

    for p in patients.values() if isinstance(patients, dict) else patients:
        cur.execute("""
            INSERT INTO patients (
                patient_id, name, age, symptoms, room,
                vitals, diagnosis, specialist, medication,
                discharged, lab_results, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p.patient_id,
            p.name,
            p.age,
            p.symptoms,
            p.room,
            json.dumps(p.vitals),
            p.diagnosis,
            p.specialist,
            p.medication,
            int(p.discharged),
            p.lab_results,
            json.dumps(p.notes)
        ))

    conn.commit()
    conn.close()



# API ROUTES

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    patient_id = system.register_patient(data["name"], data["age"])
    return jsonify({"patient_id": patient_id})

@app.post("/symptoms")
def symptoms():
    data = request.json
    return jsonify({"success": system.enter_person_info_and_symptoms(data["patient_id"], data["symptoms"])})

@app.post("/move")
def move():
    data = request.json
    return jsonify({"success": system.move_patient_room(data["patient_id"], data["new_room"])})

# UNPACK DB
@app.get("/patients/load")
def get_patients():
    print("PATIENT COUNT:", len(system.patients))
    print("PATIENTS:", system.patients)
    return jsonify({pid: p.__dict__ for pid, p in system.patients.items()})

# SAVE UPDATED TABLE TO DB
@app.route("/patients/save", methods=["POST"])
def save_patients():
    data = request.get_json()

    # --- STEP 1: Normalize name ---
    first = data.get("name", {}).get("first", "")
    last = data.get("name", {}).get("last", "")
    full_name = f"{first} {last}".strip()

    # --- STEP 2: Age  ---
    age = 0  # placeholder 

    # --- STEP 3: Create patient ---
    patient_id = system.register_patient(full_name, age)

    # --- STEP 4: Symptoms ---
    system.enter_person_info_and_symptoms(
        patient_id,
        data.get("symptoms", "")
    )

    # --- STEP 5: Room ---
    room = data.get("admission", {}).get("room")
    if room:
        system.move_patient_room(patient_id, room)

    # --- STEP 6: Notes (optional but useful) ---
    system.patients[patient_id].notes.append(
        f"RFC: {data.get('reasonForComing', '')}"
    )

    # --- STEP 7: Persist to DB ---
    save_patients_to_db(system.patients)

    return jsonify({
        "status": "ok",
        "patient_id": patient_id
    })

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
