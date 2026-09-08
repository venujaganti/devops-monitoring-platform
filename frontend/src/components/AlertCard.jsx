import {
  AlertTriangle
} from "lucide-react";

import {
  formatDate
} from "../utils/formatters";

import StatusBadge from "./StatusBadge";

export default function AlertCard({
  alert
}) {
  return (
    <div className="alert-card">
      <div className="alert-icon">
        <AlertTriangle size={20} />
      </div>

      <div className="alert-content">
        <div className="alert-title-row">
          <h3>{alert.title}</h3>

          <StatusBadge
            status={alert.severity}
          />
        </div>

        <p>{alert.message}</p>

        <small>
          {formatDate(alert.created_at)}
        </small>
      </div>
    </div>
  );
}