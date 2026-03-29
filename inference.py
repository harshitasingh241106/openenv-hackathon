import os
from openai import OpenAI
from dotenv import load_dotenv
from environment import CustomerSupportEnv, Action

# ─── Load environment variables ───────────────────────────────────────────────
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

if not all([API_BASE_URL, MODEL_NAME, HF_TOKEN]):
    raise ValueError("Missing required environment variables. Check your .env file.")

# ─── Setup OpenAI client pointing to Hugging Face ─────────────────────────────
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

# ─── Run agent on one task ─────────────────────────────────────────────────────
def run_task(task_number: int, episodes: int = 3):
    print(f"\n{'='*50}")
    print(f"TASK {task_number} — ", end="")
    if task_number == 1:
        print("Department Routing (Easy)")
    elif task_number == 2:
        print("Department + Urgency (Medium)")
    else:
        print("Full Ticket Handling (Hard)")
    print('='*50)

    env = CustomerSupportEnv(task_number=task_number)
    total_score = 0.0

    for episode in range(episodes):
        # Reset environment — get a ticket
        obs = env.reset()
        print(f"\nEpisode {episode + 1}")
        print(f"Ticket: {obs.ticket_text[:70]}...")

        # Call the LLM with the prompt
        try:
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": obs.prompt
                    }
                ],
                max_tokens=200,
                temperature=0.1
            )
            agent_response = completion.choices[0].message.content or ""
        except Exception as e:
            print(f"API call failed: {e}")
            agent_response = "General"

        print(f"Agent response: {agent_response.strip()[:80]}")

        # Step the environment with the agent's response
        action = Action(response=agent_response)
        obs, reward, done, info = env.step(action)

        print(f"Score: {reward.score} | Feedback: {reward.feedback}")
        total_score += reward.score

    avg_score = total_score / episodes
    print(f"\nAverage score for Task {task_number}: {avg_score:.2f}")
    return avg_score


# ─── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("Customer Support Ticket Router — Baseline Inference")
    print("Model:", MODEL_NAME)
    print("API:", API_BASE_URL)

    scores = {}
    scores["task1"] = run_task(task_number=1, episodes=3)
    scores["task2"] = run_task(task_number=2, episodes=3)
    scores["task3"] = run_task(task_number=3, episodes=3)

    print(f"\n{'='*50}")
    print("FINAL BASELINE SCORES")
    print('='*50)
    for task, score in scores.items():
        print(f"{task}: {score:.2f}")
    overall = sum(scores.values()) / len(scores)
    print(f"Overall average: {overall:.2f}")


if __name__ == "__main__":
    main()