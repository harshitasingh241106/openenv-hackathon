from data.tickets import TICKETS

TASK3_DESCRIPTION = """
You are a customer support router.
Read the ticket below and reply in exactly this format:
Department: <department>
Urgency: <urgency>
Reply: <your suggested reply to the customer>

For Department choose from: Billing, Technical, General
For Urgency choose from: Low, Medium, High
For Reply: write a professional, helpful response to the customer in 1-2 sentences.

Ticket: {ticket_text}

Reply in the exact format shown. No extra explanation.
"""

def get_task3_tickets():
    return TICKETS

def grade_task3(ticket_id, agent_answer):
    """
    Scores the agent on department, urgency, and reply quality.
    0.3 points for correct department
    0.3 points for correct urgency
    0.4 points for reply quality (keyword matching)
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
    agent_answer_lower = agent_answer.lower()

    correct_department = correct["department"].lower()
    correct_urgency = correct["urgency"].lower()
    correct_reply = correct["suggested_reply"].lower()

    # Check department — 0.3 points
    if correct_department in agent_answer_lower:
        score += 0.3

    # Check urgency — 0.3 points
    if correct_urgency in agent_answer_lower:
        score += 0.3

    # Check reply quality — 0.4 points
    # Extract the reply part from agent's answer
    reply_part = ""
    for line in agent_answer.split("\n"):
        if line.lower().startswith("reply:"):
            reply_part = line.replace("Reply:", "").replace("reply:", "").strip().lower()
            break

    if reply_part:
        # Get keywords from the correct reply
        # Filter out common words, keep meaningful ones
        stop_words = {"the", "a", "an", "is", "are", "we", "you", "your",
                      "our", "in", "on", "at", "to", "for", "of", "and",
                      "or", "it", "this", "that", "will", "can", "if",
                      "please", "with", "from", "have", "has", "be"}

        correct_keywords = [
            word for word in correct_reply.split()
            if word not in stop_words and len(word) > 3
        ]

        if correct_keywords:
            # Count how many keywords appear in the agent's reply
            matched = sum(
                1 for word in correct_keywords
                if word in reply_part
            )
            keyword_score = matched / len(correct_keywords)
            # Give up to 0.4 points based on keyword overlap
            score += 0.4 * keyword_score

    return round(score, 2)