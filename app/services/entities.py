import re
from typing import Dict, Any

EMAIL_RE = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")
TICKET_RE = re.compile(r"\b(?:INC|SR|CHG)\d{4,10}\b", re.IGNORECASE)

def extract_entities(text: str) -> Dict[str, Any]:
    entities: Dict[str, Any] = {}

    email = EMAIL_RE.search(text)
    if email:
        entities["email"] = email.group(0)

    ticket = TICKET_RE.search(text)
    if ticket:
        entities["ticket_id"] = ticket.group(0).upper()

    # system (heurística simples)
    lowered = text.lower()
    systems = []
    if "vpn" in lowered:
        systems.append("VPN")
    if "outlook" in lowered or "email" in lowered or "e-mail" in lowered:
        systems.append("EMAIL")
    if "teams" in lowered:
        systems.append("TEAMS")
    if "ad" in lowered or "active directory" in lowered:
        systems.append("AD")
    if "winscp" in lowered or "sftp" in lowered or "ssh" in lowered:
        systems.append("SFTP")

    if systems:
        entities["systems"] = systems

    # urgency (bem básico)
    if any(k in lowered for k in ["urgente", "parou", "sem acesso", "critico", "crítico"]):
        entities["urgency"] = "HIGH"
    elif any(k in lowered for k in ["quando puder", "não é urgente", "depois"]):
        entities["urgency"] = "LOW"

    return entities