from typing import Dict, Any
import random

class ServiceDeskConnector:
    """
    Mock de Service Desk (ex.: Jira Service Management, ServiceNow, GLPI, Freshservice etc.)
    """
    def open_ticket(self, user_id: str, summary: str, details: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        ticket_id = f"INC{random.randint(100000, 999999)}"
        return {
            "ticket_id": ticket_id,
            "status": "OPEN",
            "queue": "IT-SUPPORT",
        }

    def get_ticket_status(self, ticket_id: str) -> Dict[str, Any]:
        # Mock simples
        return {
            "ticket_id": ticket_id,
            "status": random.choice(["OPEN", "IN_PROGRESS", "WAITING_USER", "RESOLVED"]),
            "last_update": "mock",
        }