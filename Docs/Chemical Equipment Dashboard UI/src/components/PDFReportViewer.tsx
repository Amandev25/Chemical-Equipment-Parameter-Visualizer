import { Layout } from './Layout';
import { Download, Printer, Share2, ArrowLeft, FileText } from 'lucide-react';
import { Button } from './ui/button';
import { useNavigate, useParams } from 'react-router-dom';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const typeDistribution = [
  { type: 'Pump', count: 45 },
  { type: 'Reactor', count: 28 },
  { type: 'Heat Exchanger', count: 32 },
  { type: 'Compressor', count: 18 },
  { type: 'Valve', count: 67 },
];

const trendData = [
  { month: 'Jan', value: 120 },
  { month: 'Feb', value: 135 },
  { month: 'Mar', value: 145 },
  { month: 'Apr', value: 138 },
  { month: 'May', value: 142 },
  { month: 'Jun', value: 128 },
];

export function PDFReportViewer() {
  const navigate = useNavigate();
  const { id } = useParams();

  return (
    <Layout>
      <div className="space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button
              variant="outline"
              size="sm"
              onClick={() => navigate('/history')}
              className="gap-2"
            >
              <ArrowLeft className="w-4 h-4" />
              Back to History
            </Button>
            <div>
              <h1 className="text-slate-900 dark:text-white mb-1">Equipment Analysis Report</h1>
              <p className="text-slate-600 dark:text-slate-400">
                Generated on November 12, 2024 at 14:30
              </p>
            </div>
          </div>
          <div className="flex gap-3">
            <Button variant="outline" className="gap-2">
              <Share2 className="w-4 h-4" />
              Share
            </Button>
            <Button variant="outline" className="gap-2">
              <Printer className="w-4 h-4" />
              Print
            </Button>
            <Button className="gap-2 bg-gradient-to-r from-blue-500 to-teal-500 hover:from-blue-600 hover:to-teal-600">
              <Download className="w-4 h-4" />
              Download PDF
            </Button>
          </div>
        </div>

        {/* PDF Preview Container */}
        <div className="bg-slate-100 dark:bg-slate-900 rounded-2xl p-8">
          <div className="max-w-4xl mx-auto bg-white dark:bg-slate-800 rounded-xl shadow-2xl overflow-hidden">
            {/* Report Header */}
            <div className="bg-gradient-to-r from-blue-500 to-teal-500 p-8 text-white">
              <div className="flex items-center gap-4 mb-4">
                <div className="w-16 h-16 rounded-2xl bg-white/20 backdrop-blur-sm flex items-center justify-center">
                  <FileText className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h2 className="text-white mb-1">Chemical Equipment Analysis Report</h2>
                  <p className="text-white/80">Comprehensive Performance Overview</p>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-4 pt-4 border-t border-white/20">
                <div>
                  <p className="text-white/80 mb-1">Report ID</p>
                  <p className="text-white">RPT-{id}-2024</p>
                </div>
                <div>
                  <p className="text-white/80 mb-1">Period</p>
                  <p className="text-white">Nov 1-12, 2024</p>
                </div>
                <div>
                  <p className="text-white/80 mb-1">Facility</p>
                  <p className="text-white">Plant A - Main</p>
                </div>
              </div>
            </div>

            {/* Report Content */}
            <div className="p-8 space-y-8">
              {/* Executive Summary */}
              <section>
                <h3 className="text-slate-900 dark:text-white mb-4 pb-2 border-b border-slate-200 dark:border-slate-700">
                  Executive Summary
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="bg-blue-50 dark:bg-blue-900/20 rounded-xl p-4 border border-blue-200 dark:border-blue-800">
                    <p className="text-blue-600 dark:text-blue-400 mb-1">Total Equipment</p>
                    <div className="text-blue-900 dark:text-blue-300">190</div>
                  </div>
                  <div className="bg-teal-50 dark:bg-teal-900/20 rounded-xl p-4 border border-teal-200 dark:border-teal-800">
                    <p className="text-teal-600 dark:text-teal-400 mb-1">Avg Flowrate</p>
                    <div className="text-teal-900 dark:text-teal-300">136.4 L/min</div>
                  </div>
                  <div className="bg-orange-50 dark:bg-orange-900/20 rounded-xl p-4 border border-orange-200 dark:border-orange-800">
                    <p className="text-orange-600 dark:text-orange-400 mb-1">Avg Pressure</p>
                    <div className="text-orange-900 dark:text-orange-300">88.7 PSI</div>
                  </div>
                  <div className="bg-purple-50 dark:bg-purple-900/20 rounded-xl p-4 border border-purple-200 dark:border-purple-800">
                    <p className="text-purple-600 dark:text-purple-400 mb-1">Avg Temperature</p>
                    <div className="text-purple-900 dark:text-purple-300">82.3 °C</div>
                  </div>
                </div>
              </section>

              {/* Key Findings */}
              <section>
                <h3 className="text-slate-900 dark:text-white mb-4 pb-2 border-b border-slate-200 dark:border-slate-700">
                  Key Findings
                </h3>
                <ul className="space-y-3 text-slate-600 dark:text-slate-400">
                  <li className="flex items-start gap-3">
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-2"></span>
                    <span>Equipment performance maintained within optimal parameters across all facilities</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="w-1.5 h-1.5 rounded-full bg-teal-500 mt-2"></span>
                    <span>Flowrate efficiency improved by 5.2% compared to previous period</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="w-1.5 h-1.5 rounded-full bg-orange-500 mt-2"></span>
                    <span>Three equipment units flagged for preventive maintenance scheduling</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="w-1.5 h-1.5 rounded-full bg-purple-500 mt-2"></span>
                    <span>Temperature control systems operating with 98.5% reliability</span>
                  </li>
                </ul>
              </section>

              {/* Charts */}
              <section>
                <h3 className="text-slate-900 dark:text-white mb-4 pb-2 border-b border-slate-200 dark:border-slate-700">
                  Equipment Distribution
                </h3>
                <div className="bg-slate-50 dark:bg-slate-700/30 rounded-xl p-6">
                  <ResponsiveContainer width="100%" height={250}>
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
              </section>

              <section>
                <h3 className="text-slate-900 dark:text-white mb-4 pb-2 border-b border-slate-200 dark:border-slate-700">
                  Performance Trends
                </h3>
                <div className="bg-slate-50 dark:bg-slate-700/30 rounded-xl p-6">
                  <ResponsiveContainer width="100%" height={250}>
                    <LineChart data={trendData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                      <XAxis dataKey="month" stroke="#64748b" />
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
                        dataKey="value" 
                        stroke="#14b8a6" 
                        strokeWidth={3}
                        dot={{ fill: '#14b8a6', r: 4 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </section>

              {/* Recommendations */}
              <section>
                <h3 className="text-slate-900 dark:text-white mb-4 pb-2 border-b border-slate-200 dark:border-slate-700">
                  Recommendations
                </h3>
                <div className="space-y-3">
                  <div className="bg-blue-50 dark:bg-blue-900/20 rounded-xl p-4 border border-blue-200 dark:border-blue-800">
                    <div className="text-blue-900 dark:text-blue-300 mb-1">Operational Efficiency</div>
                    <p className="text-blue-700 dark:text-blue-400">
                      Continue current maintenance schedule to maintain performance levels
                    </p>
                  </div>
                  <div className="bg-orange-50 dark:bg-orange-900/20 rounded-xl p-4 border border-orange-200 dark:border-orange-800">
                    <div className="text-orange-900 dark:text-orange-300 mb-1">Preventive Action</div>
                    <p className="text-orange-700 dark:text-orange-400">
                      Schedule inspection for Reactor-B-205 and Compressor-D-102
                    </p>
                  </div>
                  <div className="bg-teal-50 dark:bg-teal-900/20 rounded-xl p-4 border border-teal-200 dark:border-teal-800">
                    <div className="text-teal-900 dark:text-teal-300 mb-1">Monitoring</div>
                    <p className="text-teal-700 dark:text-teal-400">
                      Increase data collection frequency for critical equipment
                    </p>
                  </div>
                </div>
              </section>

              {/* Footer */}
              <section className="pt-6 border-t border-slate-200 dark:border-slate-700">
                <p className="text-slate-500 dark:text-slate-400 text-center">
                  Report generated by ChemViz Pro • Confidential • For internal use only
                </p>
              </section>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
