# hospital_crew.py
from agents import triage_agent, investigator_agent, resolve_agent
from tools import (
    FetchPatientInfoTool,
    CheckRoomStatusTool,
    CheckInventoryItemTool,
    SendMessageToStaffTool,
    EscalateToHumanTool,
    LogComplaintTool,
)
from typing import Dict, Any

# instantiate tools
fetch_tool = FetchPatientInfoTool()
room_tool = CheckRoomStatusTool()
inventory_tool = CheckInventoryItemTool()
send_tool = SendMessageToStaffTool()
escalate_tool = EscalateToHumanTool()
log_tool = LogComplaintTool()

# Default provider choices for each agent (you can change to 'groq','together','huggingface','openai')
TRIAGE_PROVIDER = "groq"
INVESTIGATOR_PROVIDER = "together"
RESOLUTION_PROVIDER = "openai"
FALLBACKS = ["openai", "huggingface", "groq", "together"]  # order of fallbacks

def process_complaint(user_input: str) -> Dict[str, Any]:
    steps = []
    try:
        # 1) Triage
        triage = triage_agent(user_input, provider=TRIAGE_PROVIDER, fallbacks=FALLBACKS)
        steps.append({"agent":"Triage", "status":"completed" if triage else "failed", "output": triage})

        # 2) Investigation (use tools)
        # Extract potential room/item/patient from triage if available
        room_num = None
        item = None
        patient_name = None
        if isinstance(triage, dict):
            room_num = triage.get("room_number") or triage.get("room") or triage.get("room_number", None)
            item = None
            # try issue detail detection
            issue = triage.get("issue_details") or triage.get("issue", None)
            if isinstance(issue, str):
                if "pillow" in issue.lower():
                    item = "pillow"

            # Try patient
            p = triage.get("patient_info")
            if isinstance(p, dict):
                patient_name = p.get("name")

        # call tools
        tools_data = {}
        if patient_name:
            tools_data["fetch_patient"] = fetch_tool._run(patient_name)
        if room_num:
            tools_data["check_room"] = room_tool._run(str(room_num))
        if item:
            tools_data["check_inventory"] = inventory_tool._run(item)

        investigator = investigator_agent(triage, tools_data, provider=INVESTIGATOR_PROVIDER, fallbacks=FALLBACKS)
        steps.append({"agent":"Investigation", "status":"completed" if investigator else "failed", "output": investigator})

        # 3) Resolution: perform actions using tools depending on facts
        # Build tools_results dictionary with concrete actions
        actions = []
        tools_results = {}
        # example: if item available -> send message to housekeeping
        try:
            availability = investigator.get("item_availability") if isinstance(investigator, dict) else None
        except Exception:
            availability = None

        # Decide department
        department = "housekeeping" if (item or (investigator and "pillow" in str(investigator).lower())) else "general"

        # Example action: send message
        msg = f"Please deliver pillow to Room {room_num} ASAP." if room_num else "Please check the request."
        send_res = send_tool._run(department, msg)
        actions.append({"send_message": send_res})
        tools_results["send_message"] = send_res

        # Log complaint
        log_res = log_tool._run(patient_name or "anonymous", f"{user_input}")
        actions.append({"log_complaint": log_res})
        tools_results["log_complaint"] = log_res

        # Optionally escalate if urgent
        urgency = None
        if isinstance(triage, dict):
            urgency = triage.get("urgency")
        if urgency and str(urgency).lower() in ("high", "urgent", "1", "0"):
            esc = escalate_tool._run("general", f"Urgent: {user_input}")
            actions.append({"escalate": esc})
            tools_results["escalate"] = esc

        resolution = resolve_agent(triage, investigator, tools_results, provider=RESOLUTION_PROVIDER, fallbacks=FALLBACKS)
        # ensure we have final_message
        final_msg = resolution.get("final_message") if isinstance(resolution, dict) else str(resolution)
        steps.append({"agent":"Resolution", "status":"completed" if resolution else "failed", "output": resolution})

        return {"final": final_msg, "steps": steps, "actions": actions}

    except Exception as e:
        return {"final": f"❌ Error while processing complaint: {e}", "steps": steps, "actions": []}
