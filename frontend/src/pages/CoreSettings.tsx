import React, { useState } from "react";
import { RebeccaCoreService } from "../services/RebeccaCoreService";

type StatusVariant = "idle" | "connected" | "failed" | "error";

export const CoreSettings: React.FC = () => {
  const [endpoint, setEndpoint] = useState("http://localhost:8000");
  const [token, setToken] = useState("");
  const [status, setStatus] = useState<StatusVariant>("idle");
  const [isTesting, setIsTesting] = useState(false);

  const labelForStatus: Record<StatusVariant, string> = {
    idle: "Awaiting test",
    connected: "Connected",
    failed: "Failed",
    error: "Error",
  };

  const handleTestConnection = async () => {
    setIsTesting(true);
    try {
      const result = await RebeccaCoreService.testConnection(endpoint, token);
      setStatus(result ? "connected" : "failed");
    } catch (error) {
      console.error(error);
      setStatus("error");
    } finally {
      setIsTesting(false);
    }
  };

  return (
    <section className="core-settings">
      <header>
        <h2>Rebecca Core Connection</h2>
        <p>Configure endpoint and credentials to link DROId with Rebecca core services.</p>
      </header>
      <div className="form-group">
        <label htmlFor="core-endpoint">Endpoint</label>
        <input
          id="core-endpoint"
          value={endpoint}
          onChange={(event) => setEndpoint(event.target.value)}
          placeholder="http://localhost:8000"
        />
      </div>
      <div className="form-group">
        <label htmlFor="core-token">Token</label>
        <input
          id="core-token"
          value={token}
          onChange={(event) => setToken(event.target.value)}
          type="password"
        />
      </div>
      <div className="actions">
        <button onClick={handleTestConnection} disabled={isTesting}>
          {isTesting ? "Testing..." : "Test Connection"}
        </button>
        <span className={`status status-${status}`}>{labelForStatus[status]}</span>
      </div>
    </section>
  );
};