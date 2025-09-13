# tools.py
from crewai.tools import BaseTool

class FetchPatientInfoTool(BaseTool):
    name: str = "Fetch Patient Information"
    description: str = "Fetches patient information from the hospital database using patient ID or name."
    
    def _run(self, patient_id: str) -> str:
        print(f"[TOOL] Fetching info for patient: {patient_id}")
        pid = str(patient_id).lower()
        if "john doe" in pid:
            return "Patient John Doe confirmed in Room 205. Admitted today for observation. Patient ID: JD-205-0924."
        elif "jane smith" in pid:
            return "Patient Jane Smith in Room 304. Admitted yesterday. Patient ID: JS-304-0924."
        else:
            return f"Patient {patient_id} not found in main database. Checking secondary records..."

class CheckRoomStatusTool(BaseTool):
    name: str = "Check Room Status"
    description: str = "Checks the current status of a hospital room (occupied, available, cleaning status, etc.)."
    
    def _run(self, room_number: str) -> str:
        print(f"[TOOL] Checking status for room: {room_number}")
        room_statuses = {
            "205": "Room 205: Occupied by John Doe. Last cleaned: 2 hours ago.",
            "304": "Room 304: Occupied by Jane Smith. Maintenance scheduled tomorrow.",
            "101": "Room 101: Available. Ready for new patient.",
            "102": "Room 102: Currently being cleaned. Available in 30 minutes."
        }
        return room_statuses.get(str(room_number), f"Room {room_number} status: Unknown. Please check with floor staff.")

class CheckInventoryItemTool(BaseTool):
    name: str = "Check Inventory Item"
    description: str = "Checks the availability and stock level of specific items in hospital inventory."
    
    def _run(self, item_name: str) -> str:
        print(f"[TOOL] Checking inventory for: {item_name}")
        inventory = {
            "pillow": "Pillows: 42 in stock (Main storage). 5 available on Floor 2.",
            "blanket": "Blankets: 38 in stock. 10 warm blankets available.",
            "medicine": "General medicine cabinet: Well stocked. Specific medicines require pharmacist approval.",
            "lunch tray": "Lunch trays: Available. Kitchen has 50+ ready for service."
        }
        item_lower = str(item_name).lower()
        for key, value in inventory.items():
            if key in item_lower:
                return value
        return f"Inventory for {item_name}: Not found in main system. Please check with supplies department."

class SendMessageToStaffTool(BaseTool):
    name: str = "Send Message to Staff"
    description: str = "Sends messages to hospital staff departments (kitchen, housekeeping, nursing, maintenance)."
    
    def _run(self, department: str, message: str) -> str:
        print(f"\n[TOOL] SENDING MESSAGE to {department.upper()}: '{message}'")
        departments = {
            "kitchen": f"Message acknowledged by Kitchen staff. Ticket #K{hash(message) % 1000} created.",
            "housekeeping": f"Housekeeping notified. Task assigned to team. Reference #H{hash(message) % 1000}",
            "nursing": f"Nursing station alert sent. Nurse assigned to follow up. Code #N{hash(message) % 1000}",
            "maintenance": f"Maintenance request logged. Technician dispatched. Ticket #M{hash(message) % 1000}"
        }
        dept_lower = department.lower()
        for key, value in departments.items():
            if key in dept_lower:
                return value
        return f"Message sent to {department}: 'ACKNOWLEDGED - {message[:50]}...'"
    
class EscalateToHumanTool(BaseTool):
    name: str = "Escalate to Human"
    description: str = "Escalates critical issues to human supervisors or managers for immediate attention."
    
    def _run(self, supervisor_role: str, issue_details: str) -> str:
        print(f"\n[TOOL] ESCALATING to {supervisor_role.upper()}: {issue_details}")
        escalation_paths = {
            "medical": "ESCALATED to Chief Medical Officer. Priority: HIGH. Case ID: MED-EMG-2024",
            "administrative": "ESCALATED to Hospital Administrator. Priority: URGENT. Ticket: ADMIN-CRIT-2024",
            "technical": "ESCALATED to IT Director. Priority: MEDIUM. Incident: TECH-SYS-2024",
            "general": f"ESCALATED to {supervisor_role}. Priority: REVIEW. Reference: GEN-{hash(issue_details) % 10000}"
        }
        for key, value in escalation_paths.items():
            if key in supervisor_role.lower():
                return value
        return f"Issue has been escalated to {supervisor_role}. Case reference: ESC-{hash(issue_details) % 10000}"
    
class LogComplaintTool(BaseTool):
    name: str = "Log Complaint"
    description: str = "Logs formal complaints in the hospital's quality assurance and tracking system."
    
    def _run(self, patient_id: str, details: str) -> str:
        print(f"[TOOL] Logging complaint for {patient_id}: {details}")
        complaint_id = f"CMP-{hash(f'{patient_id}{details}') % 10000}"
        return f"Complaint logged successfully. Reference #{complaint_id}. Quality assurance team notified."
