from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import psutil

app = FastAPI()

# CORS設定（Reactからアクセス可能にする）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 監理対象のプロセス情報
processes = {
    "frontend": None,  # npm run start:frontend 用
    "backend": None    # uvicorn backend.main:app 用
}

@app.get("/status")
def status():
    info = {}
    for name, proc in processes.items():
        info[name] = "running" if proc and psutil.pid_exists(proc.pid) else "stopped"
    return info

@app.post("/start/{target}")
def start(target: str):
    if target == "frontend":
        processes["frontend"] = subprocess.Popen(
            ["npm", "run", "start:frontend"], cwd="../frontend"
        )
    elif target == "backend":
        processes["backend"] = subprocess.Popen(
            ["uvicorn", "backend.main:app", "--reload"], cwd="../backend"
        )
    return {"message": f"{target} started"}

@app.post("/stop/{target}")
def stop(target: str):
    proc = processes.get(target)
    if proc:
        proc.terminate()
        proc.wait()
        processes[target] = None
    return {"message": f"{target} stopped"}

@app.post("/restart/{target}")
def restart(target: str):
    stop(target)
    start(target)
    return {"message": f"{target} restarted"}
