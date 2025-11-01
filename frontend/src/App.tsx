import { useEffect, useState } from "react";
import axios from "axios";

type Status = {
  frontend: string;
  backend: string;
};

// 環境変数から設定値を取得
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:9000";
const APP_NAME = import.meta.env.VITE_APP_NAME || "Local Dev Manager";
const REFRESH_INTERVAL = Number(import.meta.env.VITE_REFRESH_INTERVAL) || 2000;

export default function App() {
  const [status, setStatus] = useState<Status>({ frontend: "stopped", backend: "stopped" });

  const fetchStatus = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/status`);
      setStatus(res.data);
    } catch (error) {
      console.error("Failed to fetch status:", error);
    }
  };

  const control = async (target: string, action: "start" | "stop" | "restart") => {
    try {
      await axios.post(`${API_BASE_URL}/${action}/${target}`);
      fetchStatus();
    } catch (error) {
      console.error(`Failed to ${action} ${target}:`, error);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, REFRESH_INTERVAL);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>{APP_NAME}</h1>
      {(["frontend", "backend"] as const).map(t => (
        <div key={t} style={{ marginBottom: 10 }}>
          <span style={{ width: 100, display: "inline-block" }}>{t}: {status[t]}</span>
          <button onClick={() => control(t, "start")}>Start</button>
          <button onClick={() => control(t, "stop")}>Stop</button>
          <button onClick={() => control(t, "restart")}>Restart</button>
        </div>
      ))}
    </div>
  );
}
