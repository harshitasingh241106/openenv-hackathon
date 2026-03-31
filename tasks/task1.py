from data.tickets import TICKETS

TASK1_DESCRIPTION = """
You are a customer support router.
Read the ticket below and reply with ONLY one word — the department name.
Choose from exactly these five options: Billing, Technical, General, Security

Ticket: {ticket_text}

Reply with only one word. No explanation.
"""

def get_task1_tickets():
    return TICKETS

def grade_task1(ticket_id, agent_answer):
    correct = None
    for ticket in TICKETS:
        if ticket["id"] == ticket_id:
            correct = ticket
            break

    if correct is None:
        return 0.0

    agent_answer = agent_answer.strip().lower()
    correct_department = correct["department"].lower()

    if agent_answer == correct_department:
        return 1.0
    else:
        return 0.0