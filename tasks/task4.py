from data.tickets import TICKETS

TASK4_DESCRIPTION = """
You are a senior customer support manager.
Read the ticket below and reply in exactly this format:
Department: <department>
Urgency: <urgency>
Escalate: <Yes or No>
Reason: <one sentence explaining why you chose this department and urgency>
Reply: <professional reply to the customer in 2-3 sentences>

For Department choose from: Billing, Technical, General, Security
For Urgency choose from: Low, Medium, High
Escalate Yes if the issue requires a senior manager or immediate action, No otherwise.

Ticket: {ticket_text}

Reply in the exact format shown. No extra explanation.
"""

def get_task4_tickets():
    return TICKETS

def grade_task4(ticket_id, agent_answer):
    """
    Expert level grader.
    0.25 — correct department
    0.25 — correct urgency
    0.20 — correct escalation decision
    0.30 — reply quality (keyword match)
    Total: 0.0 to 1.0
    """
    correct = None
    for ticket in TICKETS:
        if ticket["id"] == ticket_id:
            correct = ticket
            break

    if correct is None:
        return 0.0

    score = 0.0
    agent_lower = agent_answer.lower()

    correct_department = correct["department"].lower()
    correct_urgency = correct["urgency"].lower()
    correct_reply = correct["suggested_reply"].lower()

    # Escalation should be Yes for High urgency, No otherwise
    should_escalate = correct["urgency"] == "High"

    # Department — 0.25
    if correct_department in agent_lower:
        score += 0.25

    # Urgency — 0.25
    if correct_urgency in agent_lower:
        score += 0.25

    # Escalation — 0.20
    escalate_line = ""
    for line in agent_answer.split("\n"):
        if line.lower().startswith("escalate:"):
            escalate_line = line.lower()
            break

    if escalate_line:
        agent_escalates = "yes" in escalate_line
        if agent_escalates == should_escalate:
            score += 0.20

    # Reply quality — 0.30
    reply_part = ""
    for line in agent_answer.split("\n"):
        if line.lower().startswith("reply:"):
            reply_part = line.replace("Reply:", "").replace("reply:", "").strip().lower()
            break

    if reply_part:
        stop_words = {"the", "a", "an", "is", "are", "we", "you", "your",
                      "our", "in", "on", "at", "to", "for", "of", "and",
                      "or", "it", "this", "that", "will", "can", "if",
                      "please", "with", "from", "have", "has", "be"}

        correct_keywords = [
            word for word in correct_reply.split()
            if word not in stop_words and len(word) > 3
        ]

        if correct_keywords:
            matched = sum(1 for word in correct_keywords if word in reply_part)
            score += 0.30 * (matched / len(correct_keywords))

    return round(score, 2)