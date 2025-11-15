import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { Search, Filter, Download, FileDown } from 'lucide-react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { api } from '../api/client';
import { CustomTooltip } from '../components/CustomTooltip';

export default function VisualizationPage({ onLogout }) {
  const [equipment, setEquipment] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterCsvUpload, setFilterCsvUpload] = useState('all');
  const [csvUploads, setCsvUploads] = useState([]);
  const [equipmentTypes, setEquipmentTypes] = useState([]);
  const [typeDistribution, setTypeDistribution] = useState([]);
  const [flowrateData, setFlowrateData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCsvUploads();
    fetchData();
  }, []);

  useEffect(() => {
    fetchData();
  }, [filterCsvUpload]);

  const fetchCsvUploads = async () => {
    try {
      const response = await api.getUploads();
      const uploads = response.data.results || response.data || [];
      setCsvUploads(uploads);
    } catch (error) {
      console.error('Error fetching CSV uploads:', error);
    }
  };

  const fetchData = async () => {
    try {
      setLoading(true);
      const params = filterCsvUpload !== 'all' ? { csv_upload: filterCsvUpload } : {};
      
      const [equipmentRes, typesRes, typeDistRes, flowrateRes] = await Promise.all([
        api.getEquipment(params),
        api.getEquipmentTypes(),
        api.getTypeDistributionData(params),
        api.getFlowrateChartData(params),
      ]);

      setEquipment(equipmentRes.data.results || equipmentRes.data || []);
      setEquipmentTypes(typesRes.data.types || []);

      // Format type distribution
      const typeChartData = typeDistRes.data.types?.map((type, index) => ({
        type: type,
        count: typeDistRes.data.counts?.[index] || 0,
      })) || [];
      setTypeDistribution(typeChartData);

      // Format flowrate data
      const flowrateChartData = flowrateRes.data.equipment_ids?.map((id, index) => ({
        name: id,
        flowrate: flowrateRes.data.flowrates?.[index] || 0,
      })) || [];
      setFlowrateData(flowrateChartData.slice(0, 10));
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredData = equipment.filter((item) => {
    const matchesSearch = item.equipment_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.equipment_id?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = filterType === 'all' || item.equipment_type === filterType;
    return matchesSearch && matchesType;
  });

  // Get dynamic columns from the data
  const getDynamicColumns = () => {
    if (filteredData.length === 0) return [];
    
    // Fields to exclude from display
    const excludeFields = [
      'id', 'csv_upload_id', 'created_at', 'updated_at',
      'is_operational', 'needs_maintenance', 'additional_params'
    ];
    // Note: csv_upload_filename is included in display (shown at the end)
    
    // Standard fields that should always be shown first
    const standardFields = ['equipment_name', 'equipment_type'];
    
    // Get all unique keys from the data
    const allKeys = new Set();
    filteredData.forEach(item => {
      Object.keys(item).forEach(key => {
        if (!excludeFields.includes(key)) {
          allKeys.add(key);
        }
      });
    });
    
    // Sort: standard fields first, then others alphabetically, csv_upload_filename last
    const sortedKeys = Array.from(allKeys).sort((a, b) => {
      // csv_upload_filename always goes last
      if (a === 'csv_upload_filename') return 1;
      if (b === 'csv_upload_filename') return -1;
      
      const aIndex = standardFields.indexOf(a);
      const bIndex = standardFields.indexOf(b);
      if (aIndex !== -1 && bIndex !== -1) return aIndex - bIndex;
      if (aIndex !== -1) return -1;
      if (bIndex !== -1) return 1;
      return a.localeCompare(b);
    });
    
    return sortedKeys;
  };

  const dynamicColumns = getDynamicColumns();

  // Format column name for display
  const formatColumnName = (key) => {
    return key
      .replace(/_/g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase());
  };

  const handleExportCSV = () => {
    if (filteredData.length === 0) return;
    
    // Use dynamic columns for export
    const exportColumns = dynamicColumns.length > 0 ? dynamicColumns : ['equipment_name', 'equipment_type'];
    const headers = exportColumns.map(col => formatColumnName(col));
    
    const rows = filteredData.map(item => {
      return exportColumns.map(column => {
        const value = item[column];
        // Handle null/undefined values
        if (value == null || value === '') return '';
        // Escape commas and quotes in CSV
        const stringValue = String(value);
        if (stringValue.includes(',') || stringValue.includes('"') || stringValue.includes('\n')) {
          return `"${stringValue.replace(/"/g, '""')}"`;
        }
        return stringValue;
      });
    });

    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'equipment_data.csv';
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const handleGeneratePDF = async () => {
    try {
      const response = await api.generateReport({
        type: filterType !== 'all' ? filterType : null,
      });
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'equipment_report.pdf';
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error generating PDF:', error);
      alert('Failed to generate PDF report');
    }
  };

  if (loading) {
    return (
      <Layout onLogout={onLogout}>
        <div className="flex items-center justify-center h-64">
          <div className="text-slate-500 dark:text-slate-400">Loading data...</div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout onLogout={onLogout}>
      <div className="space-y-4 h-full flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between flex-shrink-0">
          <div>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Data Visualization</h1>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Analyze equipment parameters and trends
            </p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={handleExportCSV}
              className="px-3 py-1.5 text-sm rounded-lg border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 transition-all flex items-center gap-2"
            >
              <Download className="w-4 h-4" />
              Export CSV
            </button>
            <button
              onClick={handleGeneratePDF}
              className="px-3 py-1.5 text-sm rounded-lg bg-gradient-to-r from-blue-500 to-teal-500 hover:from-blue-600 hover:to-teal-600 text-white font-semibold transition-all flex items-center gap-2"
            >
              <FileDown className="w-4 h-4" />
              Generate PDF
            </button>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white dark:bg-slate-800 rounded-xl p-4 border border-slate-200 dark:border-slate-700 flex-shrink-0">
          <div className="flex flex-wrap gap-3">
            <div className="flex-1 min-w-[200px] relative">
              <Search className="absolute left-2.5 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none z-10" />
              <input
                type="text"
                placeholder="Search equipment..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-9 pr-3 py-2 text-sm rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
              />
            </div>
            <div className="relative min-w-[200px]">
              <Filter className="absolute left-2.5 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none z-10" />
              <select
                value={filterCsvUpload}
                onChange={(e) => setFilterCsvUpload(e.target.value)}
                className="w-full pl-9 pr-8 py-2 text-sm rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all appearance-none cursor-pointer"
              >
                <option value="all">All CSV Files</option>
                {csvUploads.map((upload) => (
                  <option key={upload.id} value={upload.id}>
                    {upload.filename} ({upload.total_records || 0} records)
                  </option>
                ))}
              </select>
              <div className="absolute right-2.5 top-1/2 transform -translate-y-1/2 pointer-events-none z-10">
                <svg className="w-4 h-4 text-slate-400 dark:text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>
            <div className="relative min-w-[180px]">
              <Filter className="absolute left-2.5 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none z-10" />
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                className="w-full pl-9 pr-8 py-2 text-sm rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all appearance-none cursor-pointer"
              >
                <option value="all">All Types</option>
                {equipmentTypes.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
              <div className="absolute right-2.5 top-1/2 transform -translate-y-1/2 pointer-events-none z-10">
                <svg className="w-4 h-4 text-slate-400 dark:text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        {/* Data Table */}
        <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 overflow-hidden flex-1 flex flex-col min-h-0">
          <div className="p-3 border-b border-slate-200 dark:border-slate-700 flex-shrink-0">
            <h3 className="text-slate-900 dark:text-white font-semibold text-sm">Equipment Data</h3>
            <p className="text-slate-500 dark:text-slate-400 text-xs mt-0.5">
              {filteredData.length} equipment records
              {filterCsvUpload !== 'all' && (
                <span className="ml-2 text-blue-600 dark:text-blue-400">
                  (Filtered by: {csvUploads.find(u => u.id.toString() === filterCsvUpload)?.filename || 'Unknown'})
                </span>
              )}
            </p>
          </div>
          <div className="flex-1 overflow-auto min-h-0">
            <table className="w-full">
              <thead className="bg-slate-50 dark:bg-slate-700/50 sticky top-0 z-10">
                <tr>
                  {dynamicColumns.map((column) => (
                    <th key={column} className="text-left py-2 px-3 text-slate-600 dark:text-slate-400 font-medium text-xs whitespace-nowrap">
                      {formatColumnName(column)}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {filteredData.length === 0 ? (
                  <tr>
                    <td colSpan={dynamicColumns.length || 1} className="py-8 text-center text-slate-500 dark:text-slate-400 text-sm">
                      No equipment data found. Upload a CSV file to get started.
                    </td>
                  </tr>
                ) : (
                  filteredData.map((item) => (
                    <tr key={item.id} className="border-t border-slate-100 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700/30 transition-colors">
                      {dynamicColumns.map((column) => {
                        const value = item[column];
                        // Special handling for equipment_type
                        if (column === 'equipment_type') {
                          return (
                            <td key={column} className="py-2 px-3">
                              <span className="inline-block px-2 py-0.5 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-xs font-medium whitespace-nowrap">
                                {value || 'N/A'}
                              </span>
                            </td>
                          );
                        }
                        // Special handling for csv_upload_filename
                        if (column === 'csv_upload_filename') {
                          return (
                            <td key={column} className="py-2 px-3 text-slate-600 dark:text-slate-400">
                              <span className="inline-block px-2 py-0.5 rounded text-xs bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 font-medium max-w-[150px] truncate" title={value || 'N/A'}>
                                {value || 'N/A'}
                              </span>
                            </td>
                          );
                        }
                        // Default rendering
                        return (
                          <td key={column} className="py-2 px-3 text-slate-600 dark:text-slate-400 text-sm whitespace-nowrap">
                            {value != null && value !== '' ? (
                              typeof value === 'number' ? value.toLocaleString() : String(value)
                            ) : (
                              'N/A'
                            )}
                          </td>
                        );
                      })}
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Charts - Hidden by default to save space, can be shown if needed */}
        {false && filteredData.length > 0 && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 flex-shrink-0">
            {/* Equipment Type Distribution */}
            <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 border border-slate-200 dark:border-slate-700">
              <div className="mb-6">
                <h3 className="text-slate-900 dark:text-white mb-1 font-semibold">Equipment Type Distribution</h3>
                <p className="text-slate-500 dark:text-slate-400 text-sm">Count by type</p>
              </div>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={typeDistribution} style={{ backgroundColor: 'transparent' }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" className="dark:stroke-slate-700" />
                  <XAxis dataKey="type" stroke="#64748b" className="dark:stroke-slate-400" />
                  <YAxis stroke="#64748b" className="dark:stroke-slate-400" />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar dataKey="count" fill="#3b82f6" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Flowrate Trends */}
            <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 border border-slate-200 dark:border-slate-700">
              <div className="mb-6">
                <h3 className="text-slate-900 dark:text-white mb-1 font-semibold">Flowrate Trends</h3>
                <p className="text-slate-500 dark:text-slate-400 text-sm">Top equipment by flowrate</p>
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
                    stroke="#14b8a6"
                    strokeWidth={3}
                    dot={{ fill: '#14b8a6', r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}

