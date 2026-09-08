import { useParams } from "react-router-dom";

import {
  useFetch
} from "../hooks/useFetch";

import {
  serversApi,
  metricsApi
} from "../services/api";

import {
  useCallback
} from "react";

import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";
import StatusBadge from "../components/StatusBadge";
import MetricChart from "../components/MetricChart";

export default function ServerDetails() {
  const { id } = useParams();

  const fetchServer =
    useCallback(
      () => serversApi.get(id),
      [id]
    );

  const fetchMetrics =
    useCallback(
      () =>
        metricsApi.list({
          server_id: id
        }),
      [id]
    );

  const serverState =
    useFetch(
      fetchServer,
      [fetchServer]
    );

  const metricsState =
    useFetch(
      fetchMetrics,
      [fetchMetrics]
    );

  if (
    serverState.loading ||
    metricsState.loading
  ) {
    return <LoadingSpinner />;
  }

  if (serverState.error) {
    return (
      <ErrorMessage
        message={serverState.error}
      />
    );
  }

  const metrics =
    Array.isArray(metricsState.data)
      ? metricsState.data
      : [];

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h2>
            {serverState.data.hostname}
          </h2>

          <p>
            {serverState.data.ip_address}
          </p>
        </div>

        <StatusBadge
          status={
            serverState.data.status
          }
        />
      </div>

      <div className="detail-grid">
        <div className="detail-card">
          <strong>Environment</strong>
          <span>
            {serverState.data.environment}
          </span>
        </div>

        <div className="detail-card">
          <strong>Operating System</strong>
          <span>
            {
              serverState.data
                .operating_system
            }
          </span>
        </div>

        <div className="detail-card">
          <strong>CPU Cores</strong>
          <span>
            {serverState.data.cpu_cores}
          </span>
        </div>

        <div className="detail-card">
          <strong>Memory</strong>
          <span>
            {
              serverState.data
                .memory_total_mb
            } MB
          </span>
        </div>
      </div>

      <section className="dashboard-section">
        <h2>Metrics</h2>

        <MetricChart
          data={metrics}
          dataKey="value"
          name="Metric"
        />
      </section>
    </div>
  );
}