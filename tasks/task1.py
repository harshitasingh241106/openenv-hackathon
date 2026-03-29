from data.tickets import TICKETS

TASK1_DESCRIPTION = """
You are a customer support router.
Read the ticket below and reply with ONLY one word — the department name.
Choose from exactly these three options: Billing, Technical, General

Ticket: {ticket_text}

Reply with only one word. No explanation.
"""

def get_task1_tickets():
    return TICKETS

def grade_task1(ticket_id, agent_answer):
    """
    Scores the agent's department prediction.
    Returns a score between 0.0 and 1.0.
    """
    # Find the correct ticket
    correct = None
    for ticket in TICKETS:
        if ticket["id"] == ticket_id:
            correct = ticket
            break

    if correct is None:
        return 0.0

    # Clean up the agent's answer
    agent_answer = agent_answer.strip().lower()
    correct_department = correct["department"].lower()

    # Score: 1.0 if correct, 0.0 if wrong
    if agent_answer == correct_department:
        return 1.0
    else:
        return 0.0