from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import psutil
import os
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

app = FastAPI(title="Local Dev Manager API", version="1.0.0")

# 環境変数から設定値を取得
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
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
