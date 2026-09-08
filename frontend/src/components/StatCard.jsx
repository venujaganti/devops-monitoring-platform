export default function StatCard({
  title,
  value,
  description,
  icon: Icon
}) {
  return (
    <div className="stat-card">
      <div className="stat-card-header">
        <span>{title}</span>

        {Icon && <Icon size={22} />}
      </div>

      <div className="stat-value">
        {value}
      </div>

      {description && (
        <div className="stat-description">
          {description}
        </div>
      )}
    </div>
  );
}