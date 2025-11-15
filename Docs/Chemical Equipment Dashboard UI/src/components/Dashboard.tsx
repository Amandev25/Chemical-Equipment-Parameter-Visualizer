import { Layout } from './Layout';
import { StatsCard } from './StatsCard';
import { Package, Gauge, Activity, Thermometer, TrendingUp, AlertTriangle } from 'lucide-react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const equipmentData = [
  { type: 'Pump', count: 45 },
  { type: 'Reactor', count: 28 },
  { type: 'Heat Exchanger', count: 32 },
  { type: 'Compressor', count: 18 },
  { type: 'Valve', count: 67 },
];

const trendData = [
  { time: '00:00', flowrate: 120, pressure: 85, temp: 78 },
  { time: '04:00', flowrate: 135, pressure: 88, temp: 82 },
  { time: '08:00', flowrate: 145, pressure: 92, temp: 85 },
  { time: '12:00', flowrate: 138, pressure: 89, temp: 83 },
  { time: '16:00', flowrate: 142, pressure: 91, temp: 86 },
  { time: '20:00', flowrate: 128, pressure: 87, temp: 80 },
];

const alertData = [
  { id: 1, equipment: 'Reactor-A-101', type: 'High Pressure', severity: 'warning', time: '10 min ago' },
  { id: 2, equipment: 'Pump-B-205', type: 'Low Flowrate', severity: 'info', time: '25 min ago' },
  { id: 3, equipment: 'HX-C-403', type: 'Temperature Spike', severity: 'critical', time: '1 hour ago' },
];

const COLORS = ['#3b82f6', '#14b8a6', '#f59e0b', '#8b5cf6', '#ec4899'];

export function Dashboard() {
  return (
    <Layout>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-slate-900 dark:text-white mb-2">Dashboard Overview</h1>
          <p className="text-slate-600 dark:text-slate-400">
            Real-time monitoring of chemical equipment parameters
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatsCard
            title="Total Equipment"
            value="190"
            icon={Package}
            color="blue"
            trend={{ value: 5.2, isPositive: true }}
          />
          <StatsCard
            title="Avg Flowrate"
            value="136.4"
            unit="L/min"
            icon={Gauge}
            color="teal"
            trend={{ value: 2.1, isPositive: true }}
          />
          <StatsCard
            title="Avg Pressure"
            value="88.7"
            unit="PSI"
            icon={Activity}
            color="orange"
            trend={{ value: -1.3, isPositive: false }}
          />
          <StatsCard
            title="Avg Temperature"
            value="82.3"
            unit="°C"
            icon={Thermometer}
            color="purple"
            trend={{ value: 3.7, isPositive: true }}
          />
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Equipment Distribution */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-200 dark:border-slate-700">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-slate-900 dark:text-white mb-1">Equipment Distribution</h3>
                <p className="text-slate-500 dark:text-slate-400">By equipment type</p>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={equipmentData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="type" stroke="#64748b" />
                <YAxis stroke="#64748b" />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#1e293b', 
                    border: 'none', 
                    borderRadius: '8px',
                    color: '#fff'
                  }} 
                />
                <Bar dataKey="count" fill="url(#colorGradient)" radius={[8, 8, 0, 0]} />
                <defs>
                  <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#3b82f6" />
                    <stop offset="100%" stopColor="#14b8a6" />
                  </linearGradient>
                </defs>
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* 24hr Trends */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-200 dark:border-slate-700">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-slate-900 dark:text-white mb-1">24-Hour Trends</h3>
                <p className="text-slate-500 dark:text-slate-400">Flowrate over time</p>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="time" stroke="#64748b" />
                <YAxis stroke="#64748b" />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#1e293b', 
                    border: 'none', 
                    borderRadius: '8px',
                    color: '#fff'
                  }} 
                />
                <Line 
                  type="monotone" 
                  dataKey="flowrate" 
                  stroke="#3b82f6" 
                  strokeWidth={3}
                  dot={{ fill: '#3b82f6', r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recent Alerts */}
        <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-200 dark:border-slate-700">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-slate-900 dark:text-white mb-1">Recent Alerts</h3>
              <p className="text-slate-500 dark:text-slate-400">Equipment notifications</p>
            </div>
            <button className="text-blue-500 hover:text-blue-600">View All</button>
          </div>
          <div className="space-y-4">
            {alertData.map((alert) => (
              <div
                key={alert.id}
                className="flex items-center gap-4 p-4 rounded-xl bg-slate-50 dark:bg-slate-700/50 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
              >
                <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                  alert.severity === 'critical' ? 'bg-red-100 dark:bg-red-900/30' :
                  alert.severity === 'warning' ? 'bg-orange-100 dark:bg-orange-900/30' :
                  'bg-blue-100 dark:bg-blue-900/30'
                }`}>
                  <AlertTriangle className={`w-5 h-5 ${
                    alert.severity === 'critical' ? 'text-red-500' :
                    alert.severity === 'warning' ? 'text-orange-500' :
                    'text-blue-500'
                  }`} />
                </div>
                <div className="flex-1">
                  <div className="text-slate-900 dark:text-white">{alert.equipment}</div>
                  <p className="text-slate-500 dark:text-slate-400">{alert.type}</p>
                </div>
                <div className="text-slate-500 dark:text-slate-400">
                  {alert.time}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </Layout>
  );
}
