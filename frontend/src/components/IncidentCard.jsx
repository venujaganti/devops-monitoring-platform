import {
  CheckCircle,
  Clock,
  UserCheck,
} from "lucide-react";

import StatusBadge from "./StatusBadge";


function IncidentCard({
  incident,
  serverName,
  onUpdate,
}) {

  const acknowledge = () => {
    onUpdate(
      incident.id,
      {
        status: "acknowledged",
      },
    );
  };

  const startWork = () => {
    onUpdate(
      incident.id,
      {
        status: "in_progress",
      },
    );
  };

  const resolve = () => {

    const notes = window.prompt(
      "Enter resolution notes:",
    );

    if (notes === null) {
      return;
    }

    onUpdate(
      incident.id,
      {
        status: "resolved",
        resolution_notes: notes,
      },
    );
  };

  return (
    <div className="incident-card">

      <div className="incident-card-header">

        <div>
          <h3>
            {incident.title}
          </h3>

          <p className="incident-server">
            Server: {serverName}
          </p>
        </div>

        <StatusBadge
          status={incident.severity}
        />

      </div>

      <div className="incident-description">
        {incident.description}
      </div>

      <div className="incident-meta">

        <span>
          Status:
          {" "}
          <strong>
            {incident.status}
          </strong>
        </span>

        {incident.assigned_to && (
          <span>
            Assigned user:
            {" "}
            #{incident.assigned_to}
          </span>
        )}

        <span>
          Created:
          {" "}
          {new Date(
            incident.created_at,
          ).toLocaleString()}
        </span>

      </div>

      {incident.resolution_notes && (
        <div className="incident-resolution">
          <strong>
            Resolution:
          </strong>

          <p>
            {incident.resolution_notes}
          </p>
        </div>
      )}

      <div className="incident-actions">

        {incident.status === "open" && (
          <button
            type="button"
            onClick={acknowledge}
            className="secondary-button"
          >
            <UserCheck size={16} />
            Acknowledge
          </button>
        )}

        {(
          incident.status === "open" ||
          incident.status === "acknowledged"
        ) && (
          <button
            type="button"
            onClick={startWork}
            className="secondary-button"
          >
            <Clock size={16} />
            Start Work
          </button>
        )}

        {incident.status === "in_progress" && (
          <button
            type="button"
            onClick={resolve}
            className="primary-button"
          >
            <CheckCircle size={16} />
            Resolve
          </button>
        )}

      </div>

    </div>
  );
}

export default IncidentCard;