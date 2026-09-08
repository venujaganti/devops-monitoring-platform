import { useAuth } from "../hooks/useAuth";

export default function Settings() {
  const { user } = useAuth();

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h2>Settings</h2>
          <p>
            Platform configuration.
          </p>
        </div>
      </div>

      <div className="settings-card">
        <h3>Account</h3>

        <div className="settings-row">
          <span>Username</span>
          <strong>
            {user?.username}
          </strong>
        </div>

        <div className="settings-row">
          <span>Email</span>
          <strong>
            {user?.email}
          </strong>
        </div>

        <div className="settings-row">
          <span>Role</span>
          <strong>
            {user?.role}
          </strong>
        </div>
      </div>
    </div>
  );
}