from typing import Dict, Any, Tuple, List
from .nlu import classify_intent
from ..connectors.servicedesk import ServiceDeskConnector
from ..connectors.directory import DirectoryConnector

def orchestrate(text: str, user_id: str, metadata: Dict[str, Any]) -> Tuple[str, str, float, Dict[str, Any], List[str]]:
    intent, confidence, entities = classify_intent(text)

    actions: List[str] = []
    sd = ServiceDeskConnector()
    directory = DirectoryConnector()

    # Regras de conversa (corporativas)
    if intent == "SMALLTALK":
        return ("Perfeito. Me diga em poucas palavras qual problema de TI você está tendo (ex.: VPN, e-mail, acesso, senha).",
                intent, confidence, entities, actions)

    if intent == "RESET_PASSWORD":
        # precisa de e-mail
        if "email" not in entities:
            actions.append("ASK_EMAIL")
            return ("Entendi. Para iniciar a redefinição de senha, me informe seu e-mail corporativo.",
                    intent, confidence, entities, actions)

        res = directory.request_password_reset(entities["email"])
        actions.append("PASSWORD_RESET_REQUESTED")
        reply = f"Solicitação registrada. Um link de redefinição foi enviado para {res['email']}. Se não chegar em 5 minutos, me avise."
        return (reply, intent, confidence, entities, actions)

    if intent == "ACCESS_DENIED":
        # abre chamado + sugere dados essenciais
        summary = "Acesso negado / permissão"
        details = f"Usuário relata acesso negado. Texto: {text}"
        ticket = sd.open_ticket(user_id=user_id, summary=summary, details=details, metadata=metadata)
        actions.append("OPEN_TICKET")
        reply = (
            f"Certo. Abri o chamado {ticket['ticket_id']} para tratarmos permissões. "
            "Para acelerar, me diga: qual sistema/tela e qual mensagem de erro aparece?"
        )
        return (reply, intent, confidence, entities, actions)

    if intent == "VPN_ISSUE":
        summary = "Problema de VPN"
        details = f"Usuário relata falha de VPN. Texto: {text}"
        ticket = sd.open_ticket(user_id=user_id, summary=summary, details=details, metadata=metadata)
        actions.append("OPEN_TICKET")
        reply = (
            f"Ok. Abri o chamado {ticket['ticket_id']}. "
            "Me informe: você recebe algum código de erro? E qual cliente usa (FortiClient/AnyConnect/outro)?"
        )
        return (reply, intent, confidence, entities, actions)

    if intent == "EMAIL_ISSUE":
        summary = "Problema de e-mail"
        details = f"Usuário relata problema de e-mail. Texto: {text}"
        ticket = sd.open_ticket(user_id=user_id, summary=summary, details=details, metadata=metadata)
        actions.append("OPEN_TICKET")
        reply = (
            f"Entendido. Abri o chamado {ticket['ticket_id']}. "
            "Para diagnóstico: é envio, recebimento ou login? Acontece no Outlook e no webmail também?"
        )
        return (reply, intent, confidence, entities, actions)

    if intent == "TICKET_STATUS":
        if "ticket_id" not in entities:
            actions.append("ASK_TICKET_ID")
            return ("Consigo verificar. Me informe o número do chamado (ex.: INC123456).",
                    intent, confidence, entities, actions)

        st = sd.get_ticket_status(entities["ticket_id"])
        actions.append("GET_TICKET_STATUS")
        reply = f"Status do chamado {st['ticket_id']}: {st['status']}. Se quiser, descreva novidades do caso para eu anexar ao chamado."
        return (reply, intent, confidence, entities, actions)

    if intent == "SPEAK_HUMAN":
        actions.append("ESCALATE_HUMAN")
        return ("Certo. Vou encaminhar para um atendente. Antes, me diga rapidamente: qual urgência (alta/baixa) e qual sistema afetado?",
                intent, confidence, entities, actions)

    # Fallback (UNKNOWN)
    actions.append("FALLBACK")
    return ("Entendi parcialmente. Para eu direcionar corretamente, escolha uma opção: 1) Senha  2) Acesso negado  3) VPN  4) E-mail  5) Outro",
            intent, confidence, entities, actions)