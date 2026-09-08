import {
  useCallback
} from "react";

import {
  useFetch
} from "../hooks/useFetch";

import {
  logsApi
} from "../services/api";

import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";

export default function Logs() {
  const fetchLogs =
    useCallback(
      () => logsApi.list(),
      []
    );

  const {
    data,
    loading,
    error
  } = useFetch(
    fetchLogs,
    [fetchLogs]
  );

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <ErrorMessage message={error} />
    );
  }

  const logs =
    Array.isArray(data) ? data : [];

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h2>Logs</h2>
          <p>
            Application and infrastructure
            logs.
          </p>
        </div>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Time</th>
              <th>Level</th>
              <th>Source</th>
              <th>Message</th>
            </tr>
          </thead>

          <tbody>
            {logs.map((log) => (
              <tr key={log.id}>
                <td>
                  {new Date(
                    log.created_at
                  ).toLocaleString()}
                </td>

                <td>{log.level}</td>

                <td>{log.source}</td>

                <td>{log.message}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}