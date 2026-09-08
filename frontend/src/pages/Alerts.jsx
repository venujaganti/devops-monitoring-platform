import { useFetch } from "../hooks/useFetch";

import {
  alertsApi
} from "../services/api";

import {
  useCallback
} from "react";

import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";
import AlertCard from "../components/AlertCard";

export default function Alerts() {
  const fetchAlerts =
    useCallback(
      () => alertsApi.list(),
      []
    );

  const {
    data,
    loading,
    error
  } = useFetch(
    fetchAlerts,
    [fetchAlerts]
  );

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <ErrorMessage message={error} />
    );
  }

  const alerts =
    Array.isArray(data) ? data : [];

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h2>Alerts</h2>
          <p>
            Infrastructure alerts and
            notifications.
          </p>
        </div>
      </div>

      <div className="card-list">
        {alerts.length === 0 ? (
          <p>No alerts found.</p>
        ) : (
          alerts.map((alert) => (
            <AlertCard
              key={alert.id}
              alert={alert}
            />
          ))
        )}
      </div>
    </div>
  );
}