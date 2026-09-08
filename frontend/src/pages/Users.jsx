import { useAuth } from "../hooks/useAuth";

export default function Users() {
  const { user } = useAuth();

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h2>Users</h2>
          <p>
            User management.
          </p>
        </div>
      </div>

      <div className="detail-card">
        <strong>Current User</strong>

        <span>
          Username: {user?.username}
        </span>

        <span>
          Email: {user?.email}
        </span>

        <span>
          Role: {user?.role}
        </span>
      </div>
    </div>
  );
}