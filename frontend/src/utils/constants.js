export const API_BASE_URL =
  import.meta.env.VITE_API_URL || "/api";

export const TOKEN_KEY = "devops_monitoring_token";

export const USER_KEY = "devops_monitoring_user";

export const SERVER_STATUS = {
  ONLINE: "online",
  OFFLINE: "offline",
  WARNING: "warning",
  UNKNOWN: "unknown"
};

export const ALERT_SEVERITY = {
  INFO: "info",
  WARNING: "warning",
  CRITICAL: "critical"
};

export const INCIDENT_STATUS = {
  OPEN: "open",
  IN_PROGRESS: "in_progress",
  RESOLVED: "resolved"
};