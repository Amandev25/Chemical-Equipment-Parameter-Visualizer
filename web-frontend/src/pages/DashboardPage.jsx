import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import StatsCard from '../components/StatsCard';
import { Package, Gauge, Activity, Thermometer } from 'lucide-react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { api } from '../api/client';
import { CustomTooltip } from '../components/CustomTooltip';

export default function DashboardPage({ onLogout }) {
  const [summary, setSummary] = useState(null);
  const [flowrateData, setFlowrateData] = useState([]);
  const [typeDistribution, setTypeDistribution] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [summaryRes, flowrateRes, typeRes] = await Promise.all([
        api.getDashboardSummary(),
        api.getFlowrateChartData(),
        api.getTypeDistributionData(),
      ]);

      setSummary(summaryRes.data);
      
      // Format flowrate data for chart
      const flowrateChartData = flowrateRes.data.equipment_ids?.map((id, index) => ({
        name: id,
        flowrate: flowrateRes.data.flowrates?.[index] || 0,
      })) || [];
      setFlowrateData(flowrateChartData.slice(0, 10)); // Show top 10

      // Format type distribution data
      const typeChartData = typeRes.data.types?.map((type, index) => ({
        type: type,
        count: typeRes.data.counts?.[index] || 0,
      })) || [];
      setTypeDistribution(typeChartData);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Layout onLogout={onLogout}>
        <div className="flex items-center justify-center h-64">
          <div className="text-slate-500 dark:text-slate-400">Loading dashboard...</div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout onLogout={onLogout}>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white mb-2">Dashboard Overview</h1>
          <p className="text-slate-600 dark:text-slate-400">
            Real-time monitoring of chemical equipment parameters
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatsCard
            title="Total Equipment"
            value={summary?.total_equipment || 0}
            icon={Package}
            color="blue"
          />
          <StatsCard
            title="Avg Flowrate"
            value={summary?.avg_flowrate?.toFixed(1) || '0.0'}
            unit="L/min"
            icon={Gauge}
            color="teal"
          />
          <StatsCard
            title="Avg Pressure"
            value={summary?.avg_pressure?.toFixed(1) || '0.0'}
            unit="PSI"
            icon={Activity}
            color="orange"
          />
          <StatsCard
            title="Avg Temperature"
            value={summary?.avg_temperature?.toFixed(1) || '0.0'}
            unit="°C"
            icon={Thermometer}
            color="purple"
          />
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Equipment Distribution */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-200 dark:border-slate-700">
            <div className="mb-6">
              <h3 className="text-slate-900 dark:text-white mb-1 text-lg font-semibold">Equipment Distribution</h3>
              <p className="text-slate-500 dark:text-slate-400 text-sm">By equipment type</p>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={typeDistribution} style={{ backgroundColor: 'transparent' }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" className="dark:stroke-slate-700" />
                <XAxis dataKey="type" stroke="#64748b" className="dark:stroke-slate-400" />
                <YAxis stroke="#64748b" className="dark:stroke-slate-400" />
                <Tooltip content={<CustomTooltip />} />
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

          {/* Flowrate Chart */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-200 dark:border-slate-700">
            <div className="mb-6">
              <h3 className="text-slate-900 dark:text-white mb-1 text-lg font-semibold">Top Flowrate Equipment</h3>
              <p className="text-slate-500 dark:text-slate-400 text-sm">Flowrate by equipment</p>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={flowrateData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="name" stroke="#64748b" angle={-45} textAnchor="end" height={80} />
                <YAxis stroke="#64748b" />
                <Tooltip content={<CustomTooltip />} />
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

        {/* Empty State */}
        {(!summary || summary.total_equipment === 0) && (
          <div className="bg-white dark:bg-slate-800 rounded-2xl p-12 border border-slate-200 dark:border-slate-700 text-center">
            <p className="text-slate-500 dark:text-slate-400 mb-4">
              No equipment data available. Upload a CSV file to get started.
            </p>
            <a
              href="/upload"
              className="inline-block px-6 py-3 rounded-xl bg-gradient-to-r from-blue-500 to-teal-500 hover:from-blue-600 hover:to-teal-600 text-white font-semibold transition-all"
            >
              Upload CSV File
            </a>
          </div>
        )}
      </div>
    </Layout>
  );
}

