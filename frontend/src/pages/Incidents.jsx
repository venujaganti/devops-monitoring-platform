import { useEffect, useState } from "react";
import {
  AlertTriangle,
  CheckCircle,
  Clock,
  UserCheck,
} from "lucide-react";

import { incidentsApi, serversApi } from "../services/api";
import IncidentCard from "../components/IncidentCard";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";


function Incidents() {
  const [incidents, setIncidents] = useState([]);
  const [servers, setServers] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [statusFilter, setStatusFilter] = useState("");
  const [severityFilter, setSeverityFilter] = useState("");

  const loadIncidents = async () => {
    try {
      setLoading(true);
      setError("");

      const [incidentResponse, serverResponse] =
        await Promise.all([
          incidentsApi.list({
            incident_status: statusFilter || undefined,
            severity: severityFilter || undefined,
          }),
          serversApi.list(),
        ]);

      setIncidents(incidentResponse);
      setServers(serverResponse);
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
        "Unable to load incidents."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadIncidents();
  }, [statusFilter, severityFilter]);

  const handleUpdate = async (
    incidentId,
    payload,
  ) => {
    try {
      await incidentsApi.update(
        incidentId,
        payload,
      );

      await loadIncidents();
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to update incident."
      );
    }
  };

  const openCount = incidents.filter(
    (incident) =>
      incident.status === "open",
  ).length;

  const acknowledgedCount = incidents.filter(
    (incident) =>
      incident.status === "acknowledged",
  ).length;

  const inProgressCount = incidents.filter(
    (incident) =>
      incident.status === "in_progress",
  ).length;

  const resolvedCount = incidents.filter(
    (incident) =>
      incident.status === "resolved",
  ).length;

  const getServerName = (serverId) => {
    const server = servers.find(
      (item) => item.id === serverId,
    );

    return server?.hostname || "Unknown server";
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="page-container">

      <div className="page-header">
        <div>
          <h1>Incidents</h1>
          <p>
            Track, assign, investigate and resolve
            infrastructure incidents.
          </p>
        </div>
      </div>

      <div className="stats-grid">

        <div className="stat-card">
          <div className="stat-card-icon">
            <AlertTriangle size={22} />
          </div>

          <div>
            <span>Open</span>
            <strong>{openCount}</strong>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-card-icon">
            <UserCheck size={22} />
          </div>

          <div>
            <span>Acknowledged</span>
            <strong>{acknowledgedCount}</strong>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-card-icon">
            <Clock size={22} />
          </div>

          <div>
            <span>In Progress</span>
            <strong>{inProgressCount}</strong>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-card-icon">
            <CheckCircle size={22} />
          </div>

          <div>
            <span>Resolved</span>
            <strong>{resolvedCount}</strong>
          </div>
        </div>

      </div>

      {error && (
        <ErrorMessage message={error} />
      )}

      <div className="filters-bar">

        <select
          value={statusFilter}
          onChange={(event) =>
            setStatusFilter(event.target.value)
          }
        >
          <option value="">
            All Statuses
          </option>

          <option value="open">
            Open
          </option>

          <option value="acknowledged">
            Acknowledged
          </option>

          <option value="in_progress">
            In Progress
          </option>

          <option value="resolved">
            Resolved
          </option>
        </select>

        <select
          value={severityFilter}
          onChange={(event) =>
            setSeverityFilter(event.target.value)
          }
        >
          <option value="">
            All Severities
          </option>

          <option value="critical">
            Critical
          </option>

          <option value="high">
            High
          </option>

          <option value="medium">
            Medium
          </option>

          <option value="low">
            Low
          </option>
        </select>

      </div>

      <div className="incident-list">

        {incidents.length === 0 ? (
          <div className="empty-state">
            No incidents found.
          </div>
        ) : (
          incidents.map((incident) => (
            <IncidentCard
              key={incident.id}
              incident={incident}
              serverName={getServerName(
                incident.server_id,
              )}
              onUpdate={handleUpdate}
            />
          ))
        )}

      </div>

    </div>
  );
}

export default Incidents;