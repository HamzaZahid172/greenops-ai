type MetricCardProps = {
  title: string;
  value: string;
  description?: string;
};

function MetricCard({
  title,
  value,
  description,
}: MetricCardProps) {
  return (
    <div className="metric-card">
      <h3>{title}</h3>

      <strong>{value}</strong>

      {description && <p>{description}</p>}
    </div>
  );
}

export default MetricCard;