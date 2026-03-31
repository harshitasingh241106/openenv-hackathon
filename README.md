---
title: Customer Support Ticket Router
emoji: 🎫
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
tags:
  - openenv
---

# Customer Support Ticket Router — OpenEnv Environment

An OpenEnv environment where an AI agent reads customer support tickets
and must correctly route them by department, urgency level, and suggested reply.

## What This Environment Does

Real companies receive hundreds of support tickets daily. This environment
simulates that challenge — an AI agent must read each ticket and decide:
- Which department should handle it (Billing, Technical, General)
- How urgent it is (Low, Medium, High)
- What the suggested reply should be

## Tasks

| Task | Difficulty | Description | Max Score |
|------|-----------|-------------|-----------|
| Task 1 | Easy | Route ticket to correct department | 1.0 |
| Task 2 | Medium | Route ticket + classify urgency | 1.0 |
| Task 3 | Hard | Route + urgency + generate reply | 1.0 |
| Task 4 | Expert | Route + urgency + escalation decision + reason + reply | 1.0 |

## Baseline Scores

Tested with `meta-llama/Llama-3.1-8B-Instruct` via Hugging Face router:

| Task | Score |
|------|-------|
| Task 1 — Department Routing (Easy) | 1.00 |
| Task 2 — Department + Urgency (Medium) | 0.83 |
| Task 3 — Full Ticket Handling (Hard) | 0.69 |
| Task 4 — Expert Escalation Manager (Expert) | 0.35 |
| **Overall Average** | **0.72** |

## Observation Space

| Field | Type | Description |
|-------|------|-------------|
| ticket_id | string | Unique ticket identifier |
| ticket_text | string | The customer's message |
| task_number | integer | Which task (1, 2, or 3) |
| prompt | string | Formatted prompt for the agent |
| steps_taken | integer | Number of steps taken |
| done | boolean | Whether episode is complete |

## Action Space

| Field | Type | Description |
|-------|------|-------------|
| response | string | The agent's answer |

## Reward

- Scores range from 0.0 to 1.0
- Partial credit is given for partially correct answers
- Task 1: binary (correct department = 1.0)
- Task 2: 0.5 per correct element (department + urgency)
- Task 3: 0.3 + 0.3 + 0.4 (department + urgency + reply quality)

## Setup
```bash
git clone https://github.com/harshitasingh241106/openenv-hackathon.git
cd openenv-hackathon
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Running the API
```bash
uvicorn app:app --reload
```

Visit http://localhost:7860/docs for the interactive API explorer.

## Running the Inference Script

Create a `.env` file with:
```
API_BASE_URL=https://router.huggingface.co/v1
MODEL_NAME=meta-llama/Llama-3.1-8B-Instruct
HF_TOKEN=your_hugging_face_token
```

Then run:
```bash
python inference.py
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| / | GET | Environment info |
| /health | GET | Health check |
| /reset | POST | Start new episode |
| /step | POST | Submit agent action |
| /state | GET | Current environment state |
| /tasks | GET | List all tasks |

## Docker
```bash
docker build -t customer-support-router .
docker run -p 7860:7860 customer-support-router
```