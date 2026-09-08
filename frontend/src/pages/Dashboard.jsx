import {
  Activity,
  AlertTriangle,
  Server,
  ShieldAlert
} from "lucide-react";

import {
  useMonitoring
} from "../hooks/useMonitoring";

import {
  alertsApi,
  incidentsApi
} from "../services/api";

import {
  useEffect,
  useState
} from "react";

import StatCard from "../components/StatCard";
import ServerCard from "../components/ServerCard";
import AlertCard from "../components/AlertCard";
import IncidentCard from "../components/IncidentCard";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";

export default function Dashboard() {
  const {
    data: servers,
    loading,
    error
  } = useMonitoring();

  const [alerts, setAlerts] =
    useState([]);

  const [incidents, setIncidents] =
    useState([]);

  useEffect(() => {
    async function loadData() {
      try {
        const [
          alertData,
          incidentData
        ] = await Promise.all([
          alertsApi.list(),
          incidentsApi.list()
        ]);

        setAlerts(alertData);
        setIncidents(incidentData);
      } catch {
        // Individual widgets can fail
        // without breaking dashboard.
      }
    }

    loadData();
  }, []);

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <ErrorMessage message={error} />
    );
  }

  const serverList =
    Array.isArray(servers)
      ? servers
      : [];

  const onlineServers =
    serverList.filter(
      (server) =>
        server.status === "online"
    ).length;

  const openAlerts =
    alerts.filter(
      (alert) =>
        alert.status === "open"
    ).length;

  const openIncidents =
    incidents.filter(
      (incident) =>
        incident.status !== "resolved"
    ).length;

  return (
    <div className="dashboard">
      <div className="stats-grid">
        <StatCard
          title="Total Servers"
          value={serverList.length}
          description="Registered servers"
          icon={Server}
        />

        <StatCard
          title="Online Servers"
          value={onlineServers}
          description="Currently online"
          icon={Activity}
        />

        <StatCard
          title="Open Alerts"
          value={openAlerts}
          description="Requires attention"
          icon={AlertTriangle}
        />

        <StatCard
          title="Active Incidents"
          value={openIncidents}
          description="Unresolved incidents"
          icon={ShieldAlert}
        />
      </div>

      <section className="dashboard-section">
        <div className="section-header">
          <h2>Servers</h2>
        </div>

        <div className="server-grid">
          {serverList.length === 0 ? (
            <p>No servers registered.</p>
          ) : (
            serverList
              .slice(0, 6)
              .map((server) => (
                <ServerCard
                  key={server.id}
                  server={server}
                />
              ))
          )}
        </div>
      </section>

      <div className="dashboard-columns">
        <section className="dashboard-section">
          <div className="section-header">
            <h2>Recent Alerts</h2>
          </div>

          <div className="card-list">
            {alerts.length === 0 ? (
              <p>No alerts.</p>
            ) : (
              alerts
                .slice(0, 5)
                .map((alert) => (
                  <AlertCard
                    key={alert.id}
                    alert={alert}
                  />
                ))
            )}
          </div>
        </section>

        <section className="dashboard-section">
          <div className="section-header">
            <h2>Recent Incidents</h2>
          </div>

          <div className="card-list">
            {incidents.length === 0 ? (
              <p>No incidents.</p>
            ) : (
              incidents
                .slice(0, 5)
                .map((incident) => (
                  <IncidentCard
                    key={incident.id}
                    incident={incident}
                  />
                ))
            )}
          </div>
        </section>
      </div>
    </div>
  );
}