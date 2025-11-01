from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import psutil
import os
import json
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# プロジェクト設定を読み込み
def load_project_config():
    config_path = os.path.join(os.path.dirname(__file__), "projects.json")
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"projects": {}}

project_config = load_project_config()

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

# 監視対象のプロセス情報
processes = {
    "frontend": None,  # port 5173 Viteプロジェクト用
    "backend": None    # port 8000 APIサーバー用
}

def check_port_status(port: int) -> bool:
    """ポートが使用中かチェック（IPv4とIPv6の両方を試行）"""
    import socket
    
    # IPv4でテスト
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(('localhost', port))
            if result == 0:
                return True
    except:
        pass
    
    # IPv6でテスト
    try:
        with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(('::1', port))
            if result == 0:
                return True
    except:
        pass
    
    return False

@app.get("/status")
def status():
    """実際のポート状態をチェック"""
    result = {}
    for project_name, project in project_config["projects"].items():
        port = project["port"]
        result[project_name] = "running" if check_port_status(port) else "stopped"
    return result

@app.post("/start/{target}")
def start(target: str):
    """指定されたサービスを起動"""
    if target not in project_config["projects"]:
        return {"error": f"Project '{target}' not found in configuration"}
    
    project = project_config["projects"][target]
    port = project["port"]
    
    if not check_port_status(port):
        try:
            path = os.path.expanduser(project["path"])
            processes[target] = subprocess.Popen(
                project["start_command"],
                cwd=path,
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL
            )
            return {"message": f"{project['name']} started on port {port}"}
        except Exception as e:
            return {"error": f"Failed to start {target}: {str(e)}"}
    else:
        return {"message": f"{project['name']} already running on port {port}"}

@app.post("/stop/{target}")
def stop(target: str):
    """指定されたサービスを停止"""
    if target not in project_config["projects"]:
        return {"error": f"Project '{target}' not found in configuration"}
    
    project = project_config["projects"][target]
    port = project["port"]
    success = kill_process_on_port(port)
    
    if success:
        processes[target] = None
        return {"message": f"{project['name']} stopped (port {port})"}
    else:
        return {"message": f"No process found on port {port}"}

def kill_process_on_port(port: int) -> bool:
    """指定されたポートで動作中のプロセスを終了"""
    try:
        for proc in psutil.process_iter(['pid', 'connections']):
            try:
                for conn in proc.connections():
                    if conn.laddr.port == port:
                        proc.terminate()
                        proc.wait(timeout=3)
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False
    except:
        return False

@app.post("/restart/{target}")
def restart(target: str):
    stop_result = stop(target)
    if "error" in stop_result:
        return stop_result
    
    # 少し待ってから起動
    import time
    time.sleep(1)
    
    return start(target)

@app.get("/projects")
def get_projects():
    """設定されているプロジェクト一覧を取得"""
    return project_config["projects"]
