import React, { useEffect, useState } from "react";
import axios from "axios";

type Status = {
  frontend: string;
  backend: string;
};

export default function App() {
  const [status, setStatus] = useState<Status>({ frontend: "stopped", backend: "stopped" });

  const fetchStatus = async () => {
    const res = await axios.get("http://localhost:9000/status");
    setStatus(res.data);
  };

  const control = async (target: string, action: "start" | "stop" | "restart") => {
    await axios.post(`http://localhost:9000/${action}/${target}`);
    fetchStatus();
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 2000); // 2秒ごとに状態チェック
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Local Dev Manager</h1>
      {["frontend", "backend"].map(t => (
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
