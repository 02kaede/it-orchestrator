from typing import Tuple, Dict, Any
from .entities import extract_entities

INTENT_KEYWORDS = {
    "RESET_PASSWORD": ["reset", "redefinir senha", "senha", "desbloquear", "bloqueado", "account locked"],
    "ACCESS_DENIED": ["acesso negado", "permission denied", "sem permissão", "não tenho acesso", "forbidden"],
    "VPN_ISSUE": ["vpn", "conectar", "túnel", "tunnel", "forticlient", "anyconnect"],
    "EMAIL_ISSUE": ["outlook", "email", "e-mail", "não envia", "não recebe", "caixa postal"],
    "TICKET_STATUS": ["status do chamado", "andamento", "meu chamado", "consultar chamado", "protocolo", "inc"],
    "SPEAK_HUMAN": ["atendente", "humano", "pessoa", "fala com alguém", "transferir"],
}

SMALLTALK = ["bom dia", "boa tarde", "boa noite", "obrigado", "obrigada", "valeu"]

def classify_intent(text: str) -> Tuple[str, float, Dict[str, Any]]:
    entities = extract_entities(text)
    lowered = text.lower()

    # Smalltalk
    if any(s in lowered for s in SMALLTALK):
        return "SMALLTALK", 0.95, entities

    # Se tem ticket_id e fala de status -> prioridade
    if "ticket_id" in entities and any(k in lowered for k in ["status", "andamento", "consultar", "chamado", "protocolo"]):
        return "TICKET_STATUS", 0.92, entities

    # Keyword scoring
    best_intent = "UNKNOWN"
    best_score = 0.0

    for intent, keys in INTENT_KEYWORDS.items():
        score = 0
        for k in keys:
            if k in lowered:
                score += 1
        if score > best_score:
            best_score = float(score)
            best_intent = intent

    # Normaliza confiança
    if best_intent == "UNKNOWN":
        conf = 0.30
    else:
        conf = min(0.90, 0.55 + 0.10 * best_score)

    return best_intent, conf, entities