interface StatsCardProps {
  title: string;
  value: string;
  trend: number;
  icon: string;
  prefix?: string;
}

export default function StatsCard({ title, value, trend, icon, prefix }: StatsCardProps) {
  const isPositive = trend >= 0;

  return (
    <div className="stat-card">
      <div className="flex items-start justify-between mb-2">
        <span className="stat-label">{title}</span>
        <span className="text-2xl">{icon}</span>
      </div>
      <div className="stat-value">
        {prefix}{value}
      </div>
      <div className="flex items-center gap-1.5 mt-2">
        <span className={isPositive ? 'stat-trend-up' : 'stat-trend-down'}>
          {isPositive ? '↑' : '↓'} {Math.abs(trend)}%
        </span>
        <span className="text-xs text-gray-400">vs last month</span>
      </div>
    </div>
  );
}
