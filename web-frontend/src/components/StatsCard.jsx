export default function StatsCard({ title, value, unit, icon: Icon, trend, color }) {
  const colorClasses = {
    blue: 'from-blue-500 to-blue-600',
    teal: 'from-teal-500 to-teal-600',
    orange: 'from-orange-500 to-orange-600',
    purple: 'from-purple-500 to-purple-600',
  };

  return (
    <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm hover:shadow-lg transition-shadow border border-slate-200 dark:border-slate-700">
      <div className="flex items-start justify-between mb-4">
        <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${colorClasses[color]} flex items-center justify-center`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
        {trend && (
          <div className={`text-sm font-medium ${trend.isPositive ? 'text-green-500' : 'text-red-500'}`}>
            {trend.isPositive ? '+' : ''}{trend.value}%
          </div>
        )}
      </div>
      <div className="space-y-1">
        <p className="text-sm text-slate-500 dark:text-slate-400">{title}</p>
        <div className="flex items-baseline gap-2">
          <div className="text-2xl font-bold text-slate-900 dark:text-white">{value}</div>
          {unit && <span className="text-sm text-slate-500 dark:text-slate-400">{unit}</span>}
        </div>
      </div>
    </div>
  );
}

