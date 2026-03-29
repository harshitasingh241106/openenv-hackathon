import random
from pydantic import BaseModel
from typing import Optional
from data.tickets import TICKETS
from tasks.task1 import grade_task1, TASK1_DESCRIPTION
from tasks.task2 import grade_task2, TASK2_DESCRIPTION
from tasks.task3 import grade_task3, TASK3_DESCRIPTION


# ─── Typed Models (OpenEnv requirement) ───────────────────────────────────────

class Observation(BaseModel):
    ticket_id: str
    ticket_text: str
    task_number: int
    prompt: str
    steps_taken: int
    done: bool

class Action(BaseModel):
    response: str

class Reward(BaseModel):
    score: float
    feedback: str


# ─── The Environment ──────────────────────────────────────────────────────────

class CustomerSupportEnv:
    def __init__(self, task_number: int = 1):
        """
        task_number: 1 = Easy, 2 = Medium, 3 = Hard
        """
        if task_number not in [1, 2, 3]:
            raise ValueError("task_number must be 1, 2, or 3")

        self.task_number = task_number
        self.tickets = TICKETS
        self.current_ticket = None
        self.steps_taken = 0
        self.done = False
        self.max_steps = 1  # One ticket per episode

    def reset(self) -> Observation:
        """Start a new episode with a random ticket."""
        self.current_ticket = random.choice(self.tickets)
        self.steps_taken = 0
        self.done = False

        prompt = self._get_prompt()

        return Observation(
            ticket_id=self.current_ticket["id"],
            ticket_text=self.current_ticket["text"],
            task_number=self.task_number,
            prompt=prompt,
            steps_taken=self.steps_taken,
            done=self.done
        )

    def step(self, action: Action):
        """
        Take the agent's response, grade it, and return result.
        Returns: observation, reward, done, info
        """
        if self.done:
            raise RuntimeError("Episode is done. Please call reset() first.")

        # Grade the agent's response
        reward = self._grade(action.response)

        self.steps_taken += 1
        self.done = True  # One step per episode

        observation = Observation(
            ticket_id=self.current_ticket["id"],
            ticket_text=self.current_ticket["text"],
            task_number=self.task_number,
            prompt=self._get_prompt(),
            steps_taken=self.steps_taken,
            done=self.done
        )

        info = {
            "ticket_id": self.current_ticket["id"],
            "task_number": self.task_number,
            "steps_taken": self.steps_taken
        }

        return observation, reward, self.done, info

    def state(self) -> dict:
        """Return current environment state."""
        return {
            "task_number": self.task_number,
            "current_ticket_id": self.current_ticket["id"] if self.current_ticket else None,
            "steps_taken": self.steps_taken,
            "done": self.done,
            "total_tickets": len(self.tickets)
        }

    def _get_prompt(self) -> str:
        """Build the prompt for the current task and ticket."""
        if self.task_number == 1:
            return TASK1_DESCRIPTION.format(
                ticket_text=self.current_ticket["text"]
            )
        elif self.task_number == 2:
            return TASK2_DESCRIPTION.format(
                ticket_text=self.current_ticket["text"]
            )
        else:
            return TASK3_DESCRIPTION.format(
                ticket_text=self.current_ticket["text"]
            )

    def _grade(self, agent_response: str) -> Reward:
        """Grade the agent's response based on task number."""
        ticket_id = self.current_ticket["id"]

        if self.task_number == 1:
            score = grade_task1(ticket_id, agent_response)
            feedback = "Correct department!" if score == 1.0 else "Wrong department."

        elif self.task_number == 2:
            score = grade_task2(ticket_id, agent_response)
            if score == 1.0:
                feedback = "Correct department and urgency!"
            elif score == 0.5:
                feedback = "Got one of department/urgency correct."
            else:
                feedback = "Both department and urgency wrong."

        else:
            score = grade_task3(ticket_id, agent_response)
            if score >= 0.8:
                feedback = "Excellent! Department, urgency and reply all good."
            elif score >= 0.5:
                feedback = "Partial credit. Some elements correct."
            else:
                feedback = "Needs improvement. Most elements incorrect."

        return Reward(score=score, feedback=feedback)