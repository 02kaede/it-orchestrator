from typing import Dict, Any

class DirectoryConnector:
    """
    Mock de AD/Identity Provider
    """
    def request_password_reset(self, email: str) -> Dict[str, Any]:
        # Em cenário real: chama endpoint do IAM/ADFS/Azure AD etc.
        return {"result": "RESET_LINK_SENT", "email": email}

    def request_access_review(self, user_id: str, system: str) -> Dict[str, Any]:
        return {"result": "ACCESS_REVIEW_OPENED", "system": system, "user_id": user_id}