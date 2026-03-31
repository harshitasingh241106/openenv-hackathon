from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from environment import CustomerSupportEnv, Action

app = FastAPI(
    title="Customer Support Ticket Router",
    description="An OpenEnv environment for routing customer support tickets",
    version="1.0.0"
)

envs = {
    1: CustomerSupportEnv(task_number=1),
    2: CustomerSupportEnv(task_number=2),
    3: CustomerSupportEnv(task_number=3),
    4: CustomerSupportEnv(task_number=4)
}

class StepRequest(BaseModel):
    response: str
    task_number: int = 1

class ResetRequest(BaseModel):
    task_number: int = 1

@app.get("/")
def root():
    return {
        "name": "Customer Support Ticket Router",
        "version": "1.0.0",
        "status": "running",
        "endpoints": ["/reset", "/step", "/state", "/health"]
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/reset")
def reset(request: Optional[ResetRequest] = None):
    task_number = request.task_number if request else 1
    env = envs[task_number]
    obs = env.reset()
    return {
        "observation": obs.model_dump(),
        "status": "reset complete"
    }

@app.post("/step")
def step(request: StepRequest):
    env = envs[request.task_number]
    action = Action(response=request.response)
    try:
        obs, reward, done, info = env.step(action)
        return {
            "observation": obs.model_dump(),
            "reward": reward.model_dump(),
            "done": done,
            "info": info
        }
    except RuntimeError as e:
        return {"error": str(e), "hint": "Call /reset first"}

@app.get("/state")
def state(task_number: int = 1):
    env = envs[task_number]
    return env.state()

@app.get("/tasks")
def list_tasks():
    return {
        "tasks": [
            {"id": "task1", "name": "Department Routing", "difficulty": "easy", "description": "Route ticket to correct department"},
            {"id": "task2", "name": "Department and Urgency", "difficulty": "medium", "description": "Route ticket and classify urgency"},
            {"id": "task3", "name": "Full Ticket Handling", "difficulty": "hard", "description": "Route, classify urgency, and generate reply"},
            {"id": "task4", "name": "Expert Escalation Manager", "difficulty": "expert", "description": "Route, urgency, escalation decision, reason, and reply"}
        ]
    }

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()