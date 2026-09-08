import { useFetch } from "../hooks/useFetch";

import {
  applicationsApi
} from "../services/api";

import {
  useCallback
} from "react";

import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";
import StatusBadge from "../components/StatusBadge";

export default function Applications() {
  const fetchApplications =
    useCallback(
      () => applicationsApi.list(),
      []
    );

  const {
    data,
    loading,
    error
  } = useFetch(
    fetchApplications,
    [fetchApplications]
  );

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <ErrorMessage message={error} />
    );
  }

  const applications =
    Array.isArray(data) ? data : [];

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h2>Applications</h2>
          <p>
            Application health and status.
          </p>
        </div>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Version</th>
              <th>Port</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            {applications.map(
              (application) => (
                <tr key={application.id}>
                  <td>
                    {application.name}
                  </td>

                  <td>
                    {application.version ||
                      "-"}
                  </td>

                  <td>
                    {application.port ||
                      "-"}
                  </td>

                  <td>
                    <StatusBadge
                      status={
                        application.status
                      }
                    />
                  </td>
                </tr>
              )
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}