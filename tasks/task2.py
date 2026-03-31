from data.tickets import TICKETS

TASK2_DESCRIPTION = """
You are a customer support router.
Read the ticket below and reply in exactly this format:
Department: <department>
Urgency: <urgency>

For Department choose from: Billing, Technical, General, Security
For Urgency choose from: Low, Medium, High

Ticket: {ticket_text}

Reply in the exact format shown. No extra explanation.
"""

def get_task2_tickets():
    return TICKETS

def grade_task2(ticket_id, agent_answer):
    correct = None
    for ticket in TICKETS:
        if ticket["id"] == ticket_id:
            correct = ticket
            break

    if correct is None:
        return 0.0

    score = 0.0
    agent_answer = agent_answer.lower()
    correct_department = correct["department"].lower()
    correct_urgency = correct["urgency"].lower()

    if correct_department in agent_answer:
        score += 0.5

    if correct_urgency in agent_answer:
        score += 0.5

    return score