FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
```

Save with **Ctrl + S**.

---

## Create `requirements.txt`

We also need this file so Docker knows what to install. Create a new file called `requirements.txt` in the root folder and paste this:
```
openenv==0.1.13
openai==2.30.0
fastapi==0.135.2
uvicorn==0.42.0
pydantic==2.12.5
numpy==2.4.3
python-dotenv==1.1.0