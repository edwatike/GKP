from fastapi import FastAPI, Request
import asyncio
import subprocess

app = FastAPI()

@app.post("/prompt")
async def submit_prompt(request: Request):
    data = await request.json()
    with open("prompt_queue.txt", "w") as f:
        f.write(data["prompt"])
    return {"status": "ok"}

@app.get("/run")
async def run_bot():
    subprocess.Popen(["python3", "main.py"])
    return {"status": "started"}