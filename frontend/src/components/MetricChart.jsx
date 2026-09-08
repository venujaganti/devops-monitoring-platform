import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip
} from "recharts";

export default function MetricChart({
  data = [],
  dataKey = "value",
  name = "Metric"
}) {
  return (
    <div className="chart-container">
      <ResponsiveContainer
        width="100%"
        height={300}
      >
        <LineChart data={data}>
          <CartesianGrid
            strokeDasharray="3 3"
          />

          <XAxis dataKey="recorded_at" />

          <YAxis />

          <Tooltip />

          <Line
            type="monotone"
            dataKey={dataKey}
            name={name}
            strokeWidth={2}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}