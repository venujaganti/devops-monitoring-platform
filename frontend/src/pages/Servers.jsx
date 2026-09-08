import {
  useMonitoring
} from "../hooks/useMonitoring";

import ServerCard from "../components/ServerCard";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";

export default function Servers() {
  const {
    data,
    loading,
    error
  } = useMonitoring();

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <ErrorMessage message={error} />
    );
  }

  const servers =
    Array.isArray(data)
      ? data
      : [];

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h2>Servers</h2>
          <p>
            Monitor infrastructure servers.
          </p>
        </div>
      </div>

      <div className="server-grid">
        {servers.length === 0 ? (
          <p>No servers found.</p>
        ) : (
          servers.map((server) => (
            <ServerCard
              key={server.id}
              server={server}
            />
          ))
        )}
      </div>
    </div>
  );
}