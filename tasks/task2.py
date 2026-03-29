from data.tickets import TICKETS

TASK2_DESCRIPTION = """
You are a customer support router.
Read the ticket below and reply in exactly this format:
Department: <department>
Urgency: <urgency>

For Department choose from: Billing, Technical, General
For Urgency choose from: Low, Medium, High

Ticket: {ticket_text}

Reply in the exact format shown. No extra explanation.
"""

def get_task2_tickets():
    return TICKETS

def grade_task2(ticket_id, agent_answer):
    """
    Scores the agent on both department and urgency.
    0.5 points for correct department
    0.5 points for correct urgency
    Total: 0.0 to 1.0
    """
    # Find the correct ticket
    correct = None
    for ticket in TICKETS:
        if ticket["id"] == ticket_id:
            correct = ticket
            break

    if correct is None:
        return 0.0

    score = 0.0

    # Parse agent's answer
    agent_answer = agent_answer.lower()
    correct_department = correct["department"].lower()
    correct_urgency = correct["urgency"].lower()

    # Check department — 0.5 points
    if correct_department in agent_answer:
        score += 0.5

    # Check urgency — 0.5 points
    if correct_urgency in agent_answer:
        score += 0.5

    return score
