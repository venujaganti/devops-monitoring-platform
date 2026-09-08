import {
  LayoutDashboard,
  Server,
  Boxes,
  Bell,
  AlertTriangle,
  FileText,
  Users,
  Settings,
  LogOut
} from "lucide-react";

import {
  NavLink
} from "react-router-dom";

import { useAuth } from "../hooks/useAuth";

const menuItems = [
  {
    path: "/",
    label: "Dashboard",
    icon: LayoutDashboard
  },
  {
    path: "/servers",
    label: "Servers",
    icon: Server
  },
  {
    path: "/applications",
    label: "Applications",
    icon: Boxes
  },
  {
    path: "/alerts",
    label: "Alerts",
    icon: Bell
  },
  {
    path: "/incidents",
    label: "Incidents",
    icon: AlertTriangle
  },
  {
    path: "/logs",
    label: "Logs",
    icon: FileText
  },
  {
    path: "/users",
    label: "Users",
    icon: Users
  },
  {
    path: "/settings",
    label: "Settings",
    icon: Settings
  }
];

export default function Sidebar() {
  const { logout } = useAuth();

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="logo-icon">
          D
        </div>

        <div>
          <h2>DevOps</h2>
          <span>Monitoring</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === "/"}
              className={({ isActive }) =>
                isActive
                  ? "nav-item active"
                  : "nav-item"
              }
            >
              <Icon size={19} />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      <button
        className="logout-button"
        onClick={logout}
      >
        <LogOut size={19} />
        Logout
      </button>
    </aside>
  );
}