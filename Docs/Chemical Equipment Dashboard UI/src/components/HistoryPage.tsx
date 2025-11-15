import { Layout } from './Layout';
import { Calendar, FileText, TrendingUp, Eye, Download } from 'lucide-react';
import { Button } from './ui/button';
import { useNavigate } from 'react-router-dom';

const historyData = [
  {
    id: 1,
    fileName: 'equipment_data_nov_2024.csv',
    uploadDate: 'Nov 12, 2024 14:30',
    equipmentCount: 190,
    avgFlowrate: 136.4,
    avgPressure: 88.7,
    avgTemp: 82.3,
  },
  {
    id: 2,
    fileName: 'quarterly_review_Q3.csv',
    uploadDate: 'Oct 28, 2024 09:15',
    equipmentCount: 185,
    avgFlowrate: 132.8,
    avgPressure: 87.2,
    avgTemp: 81.5,
  },
  {
    id: 3,
    fileName: 'plant_A_equipment_oct.csv',
    uploadDate: 'Oct 15, 2024 16:45',
    equipmentCount: 175,
    avgFlowrate: 128.3,
    avgPressure: 86.5,
    avgTemp: 79.8,
  },
  {
    id: 4,
    fileName: 'maintenance_check_data.csv',
    uploadDate: 'Sep 30, 2024 11:20',
    equipmentCount: 180,
    avgFlowrate: 130.1,
    avgPressure: 87.8,
    avgTemp: 80.9,
  },
  {
    id: 5,
    fileName: 'summer_performance_audit.csv',
    uploadDate: 'Sep 15, 2024 13:00',
    equipmentCount: 178,
    avgFlowrate: 129.5,
    avgPressure: 86.9,
    avgTemp: 83.2,
  },
];

export function HistoryPage() {
  const navigate = useNavigate();

  return (
    <Layout>
      <div className="space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-slate-900 dark:text-white mb-2">Upload History</h1>
            <p className="text-slate-600 dark:text-slate-400">
              View and manage your uploaded datasets
            </p>
          </div>
          <Button 
            onClick={() => navigate('/upload')}
            className="bg-gradient-to-r from-blue-500 to-teal-500 hover:from-blue-600 hover:to-teal-600"
          >
            Upload New Dataset
          </Button>
        </div>

        {/* Statistics Summary */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-gradient-to-br from-blue-500 to-teal-500 rounded-2xl p-6 text-white">
            <FileText className="w-8 h-8 mb-3 opacity-80" />
            <div className="text-white mb-1">Total Uploads</div>
            <div className="text-white">{historyData.length}</div>
          </div>
          <div className="bg-gradient-to-br from-orange-500 to-pink-500 rounded-2xl p-6 text-white">
            <TrendingUp className="w-8 h-8 mb-3 opacity-80" />
            <div className="text-white mb-1">Total Equipment</div>
            <div className="text-white">908</div>
          </div>
          <div className="bg-gradient-to-br from-purple-500 to-indigo-500 rounded-2xl p-6 text-white">
            <Calendar className="w-8 h-8 mb-3 opacity-80" />
            <div className="text-white mb-1">Last Upload</div>
            <div className="text-white">2 days ago</div>
          </div>
        </div>

        {/* History List */}
        <div className="space-y-4">
          {historyData.map((item) => (
            <div
              key={item.id}
              className="bg-white dark:bg-slate-800 rounded-2xl p-6 border border-slate-200 dark:border-slate-700 hover:shadow-lg transition-all"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-teal-500 flex items-center justify-center">
                    <FileText className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <div className="text-slate-900 dark:text-white mb-1">
                      {item.fileName}
                    </div>
                    <div className="flex items-center gap-2 text-slate-500 dark:text-slate-400">
                      <Calendar className="w-4 h-4" />
                      {item.uploadDate}
                    </div>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    className="gap-2"
                    onClick={() => navigate(`/report/${item.id}`)}
                  >
                    <Eye className="w-4 h-4" />
                    View Report
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => navigate('/visualization')}
                  >
                    Open Summary
                  </Button>
                </div>
              </div>

              {/* Quick Stats */}
              <div className="grid grid-cols-4 gap-4 pt-4 border-t border-slate-200 dark:border-slate-700">
                <div>
                  <p className="text-slate-500 dark:text-slate-400 mb-1">Equipment Count</p>
                  <div className="text-slate-900 dark:text-white">{item.equipmentCount}</div>
                </div>
                <div>
                  <p className="text-slate-500 dark:text-slate-400 mb-1">Avg Flowrate</p>
                  <div className="text-slate-900 dark:text-white">{item.avgFlowrate} L/min</div>
                </div>
                <div>
                  <p className="text-slate-500 dark:text-slate-400 mb-1">Avg Pressure</p>
                  <div className="text-slate-900 dark:text-white">{item.avgPressure} PSI</div>
                </div>
                <div>
                  <p className="text-slate-500 dark:text-slate-400 mb-1">Avg Temperature</p>
                  <div className="text-slate-900 dark:text-white">{item.avgTemp} °C</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </Layout>
  );
}
