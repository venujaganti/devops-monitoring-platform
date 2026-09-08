import { useLocation } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";

const titles = {
  "/": "Dashboard",
  "/servers": "Servers",
  "/applications": "Applications",
  "/alerts": "Alerts",
  "/incidents": "Incidents",
  "/logs": "Logs",
  "/users": "Users",
  "/settings": "Settings"
};

export default function Header() {
  const location = useLocation();
  const { user } = useAuth();

  const title =
    titles[location.pathname] ||
    "Monitoring";

  return (
    <header className="header">
      <div>
        <h1>{title}</h1>
        <p>
          DevOps Monitoring & Incident Management
        </p>
      </div>

      <div className="header-user">
        <div className="avatar">
          {user?.username
            ?.charAt(0)
            .toUpperCase()}
        </div>

        <div>
          <strong>
            {user?.full_name ||
              user?.username}
          </strong>

          <span>
            {user?.role || "viewer"}
          </span>
        </div>
      </div>
    </header>
  );
}