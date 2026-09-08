import {
  Cpu,
  MemoryStick,
  Server
} from "lucide-react";

import StatusBadge from "./StatusBadge";

export default function ServerCard({
  server,
  onClick
}) {
  return (
    <div
      className="server-card"
      onClick={onClick}
    >
      <div className="server-card-header">
        <div className="server-icon">
          <Server size={22} />
        </div>

        <StatusBadge
          status={server.status}
        />
      </div>

      <h3>{server.hostname}</h3>

      <p>{server.ip_address}</p>

      <div className="server-info">
        <span>
          <Cpu size={16} />
          {server.cpu_cores || 0} cores
        </span>

        <span>
          <MemoryStick size={16} />
          {server.memory_total_mb || 0} MB
        </span>
      </div>

      <small>
        {server.environment || "Unknown"}
      </small>
    </div>
  );
}