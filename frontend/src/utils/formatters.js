export function formatDate(date) {
  if (!date) {
    return "-";
  }

  return new Date(date).toLocaleString();
}

export function formatNumber(value, decimals = 2) {
  if (value === null || value === undefined) {
    return "-";
  }

  return Number(value).toFixed(decimals);
}

export function formatPercentage(value) {
  if (value === null || value === undefined) {
    return "-";
  }

  return `${Number(value).toFixed(1)}%`;
}

export function formatBytes(bytes) {
  if (!bytes || bytes <= 0) {
    return "0 B";
  }

  const units = ["B", "KB", "MB", "GB", "TB"];

  const index = Math.floor(
    Math.log(bytes) / Math.log(1024)
  );

  return `${(
    bytes / Math.pow(1024, index)
  ).toFixed(2)} ${units[index]}`;
}