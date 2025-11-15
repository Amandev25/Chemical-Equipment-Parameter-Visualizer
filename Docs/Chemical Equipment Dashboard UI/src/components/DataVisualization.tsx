import { useState } from 'react';
import { Layout } from './Layout';
import { Search, Filter, Download, FileDown } from 'lucide-react';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const equipmentData = [
  { id: 1, name: 'Pump-A-101', type: 'Pump', flowrate: 125, pressure: 85, temperature: 78 },
  { id: 2, name: 'Reactor-B-205', type: 'Reactor', flowrate: 145, pressure: 92, temperature: 85 },
  { id: 3, name: 'HX-C-403', type: 'Heat Exchanger', flowrate: 135, pressure: 88, temperature: 82 },
  { id: 4, name: 'Compressor-D-102', type: 'Compressor', flowrate: 115, pressure: 95, temperature: 90 },
  { id: 5, name: 'Valve-E-305', type: 'Valve', flowrate: 130, pressure: 87, temperature: 79 },
  { id: 6, name: 'Pump-F-108', type: 'Pump', flowrate: 128, pressure: 86, temperature: 80 },
  { id: 7, name: 'Reactor-G-210', type: 'Reactor', flowrate: 142, pressure: 91, temperature: 84 },
  { id: 8, name: 'HX-H-405', type: 'Heat Exchanger', flowrate: 138, pressure: 89, temperature: 83 },
];

const typeDistribution = [
  { type: 'Pump', count: 45 },
  { type: 'Reactor', count: 28 },
  { type: 'Heat Exchanger', count: 32 },
  { type: 'Compressor', count: 18 },
  { type: 'Valve', count: 67 },
];

const trendData = [
  { time: 'Jan', flowrate: 120, pressure: 85, temperature: 78 },
  { time: 'Feb', flowrate: 135, pressure: 88, temperature: 82 },
  { time: 'Mar', flowrate: 145, pressure: 92, temperature: 85 },
  { time: 'Apr', flowrate: 138, pressure: 89, temperature: 83 },
  { time: 'May', flowrate: 142, pressure: 91, temperature: 86 },
  { time: 'Jun', flowrate: 128, pressure: 87, temperature: 80 },
];

export function DataVisualization() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');

  const filteredData = equipmentData.filter(item => {
    const matchesSearch = item.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = filterType === 'all' || item.type === filterType;
    return matchesSearch && matchesType;
  });

  return (
    <Layout>
      <div className="space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-slate-900 dark:text-white mb-2">Data Visualization</h1>
            <p className="text-slate-600 dark:text-slate-400">
              Analyze equipment parameters and trends
            </p>
          </div>
          <div className="flex gap-3">
            <Button variant="outline" className="gap-2">
              <Download className="w-4 h-4" />
              Export CSV
            </Button>
            <Button className="gap-2 bg-gradient-to-r from-blue-500 to-teal-500 hover:from-blue-600 hover:to-teal-600">
              <FileDown className="w-4 h-4" />
              Generate PDF Report
            </Button>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 border border-slate-200 dark:border-slate-700">
          <div className="flex gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
              <Input
                placeholder="Search equipment..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
            <Select value={filterType} onValueChange={setFilterType}>
              <SelectTrigger className="w-64">
                <Filter className="w-4 h-4 mr-2" />
                <SelectValue placeholder="Equipment Type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Types</SelectItem>
                <SelectItem value="Pump">Pump</SelectItem>
                <SelectItem value="Reactor">Reactor</SelectItem>
                <SelectItem value="Heat Exchanger">Heat Exchanger</SelectItem>
                <SelectItem value="Compressor">Compressor</SelectItem>
                <SelectItem value="Valve">Valve</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* Data Table */}
        <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 overflow-hidden">
          <div className="p-6 border-b border-slate-200 dark:border-slate-700">
            <h3 className="text-slate-900 dark:text-white">Equipment Data</h3>
            <p className="text-slate-500 dark:text-slate-400">
              {filteredData.length} equipment records
            </p>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50 dark:bg-slate-700/50">
                <tr>
                  <th className="text-left py-4 px-6 text-slate-600 dark:text-slate-400">Equipment Name</th>
                  <th className="text-left py-4 px-6 text-slate-600 dark:text-slate-400">Type</th>
                  <th className="text-left py-4 px-6 text-slate-600 dark:text-slate-400">Flowrate (L/min)</th>
                  <th className="text-left py-4 px-6 text-slate-600 dark:text-slate-400">Pressure (PSI)</th>
                  <th className="text-left py-4 px-6 text-slate-600 dark:text-slate-400">Temperature (°C)</th>
                </tr>
              </thead>
              <tbody>
                {filteredData.map((item) => (
                  <tr key={item.id} className="border-t border-slate-100 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700/30 transition-colors">
                    <td className="py-4 px-6 text-slate-900 dark:text-white">{item.name}</td>
                    <td className="py-4 px-6">
                      <span className="px-3 py-1 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300">
                        {item.type}
                      </span>
                    </td>
                    <td className="py-4 px-6 text-slate-600 dark:text-slate-400">{item.flowrate}</td>
                    <td className="py-4 px-6 text-slate-600 dark:text-slate-400">{item.pressure}</td>
                    <td className="py-4 px-6 text-slate-600 dark:text-slate-400">{item.temperature}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Equipment Type Distribution */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 border border-slate-200 dark:border-slate-700">
            <div className="mb-6">
              <h3 className="text-slate-900 dark:text-white mb-1">Equipment Type Distribution</h3>
              <p className="text-slate-500 dark:text-slate-400">Count by type</p>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={typeDistribution}>
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
                <Bar dataKey="count" fill="#3b82f6" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Flowrate Trends */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 border border-slate-200 dark:border-slate-700">
            <div className="mb-6">
              <h3 className="text-slate-900 dark:text-white mb-1">Flowrate Trends</h3>
              <p className="text-slate-500 dark:text-slate-400">Monthly average</p>
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
                  stroke="#14b8a6" 
                  strokeWidth={3}
                  dot={{ fill: '#14b8a6', r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Pressure Trends */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 border border-slate-200 dark:border-slate-700">
            <div className="mb-6">
              <h3 className="text-slate-900 dark:text-white mb-1">Pressure Trends</h3>
              <p className="text-slate-500 dark:text-slate-400">Monthly average</p>
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
                  dataKey="pressure" 
                  stroke="#f59e0b" 
                  strokeWidth={3}
                  dot={{ fill: '#f59e0b', r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Temperature Trends */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 border border-slate-200 dark:border-slate-700">
            <div className="mb-6">
              <h3 className="text-slate-900 dark:text-white mb-1">Temperature Trends</h3>
              <p className="text-slate-500 dark:text-slate-400">Monthly average</p>
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
                  dataKey="temperature" 
                  stroke="#8b5cf6" 
                  strokeWidth={3}
                  dot={{ fill: '#8b5cf6', r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </Layout>
  );
}
