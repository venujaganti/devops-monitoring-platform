function StatusBadge({ status }) {
  const normalizedStatus =
    String(status || "")
      .toLowerCase()
      .replace("_", "-");

  return (
    <span
      className={`status-badge status-${normalizedStatus}`}
    >
      {String(status || "unknown")
        .replace("_", " ")}
    </span>
  );
}

export default StatusBadge;