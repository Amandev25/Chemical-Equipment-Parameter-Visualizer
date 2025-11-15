import { useState } from 'react';
import { Layout } from './Layout';
import { Upload, File, CheckCircle2, X } from 'lucide-react';
import { Button } from './ui/button';
import { Progress } from './ui/progress';
import { useNavigate } from 'react-router-dom';

export function CSVUpload() {
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadComplete, setUploadComplete] = useState(false);
  const navigate = useNavigate();

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.name.endsWith('.csv')) {
      setFile(droppedFile);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const handleUpload = () => {
    if (!file) return;
    
    setIsUploading(true);
    setUploadProgress(0);

    // Simulate upload progress
    const interval = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsUploading(false);
          setUploadComplete(true);
          return 100;
        }
        return prev + 10;
      });
    }, 200);
  };

  const handleReset = () => {
    setFile(null);
    setUploadComplete(false);
    setUploadProgress(0);
  };

  const mockPreviewData = [
    { name: 'Pump-A-101', type: 'Pump', flowrate: '125 L/min', pressure: '85 PSI', temp: '78°C' },
    { name: 'Reactor-B-205', type: 'Reactor', flowrate: '145 L/min', pressure: '92 PSI', temp: '85°C' },
    { name: 'HX-C-403', type: 'Heat Exchanger', flowrate: '135 L/min', pressure: '88 PSI', temp: '82°C' },
  ];

  return (
    <Layout>
      <div className="max-w-4xl mx-auto space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-slate-900 dark:text-white mb-2">Upload CSV Data</h1>
          <p className="text-slate-600 dark:text-slate-400">
            Import equipment data from CSV files
          </p>
        </div>

        {/* Upload Area */}
        {!uploadComplete ? (
          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            className={`bg-white dark:bg-slate-800 rounded-2xl p-12 border-2 border-dashed transition-all ${
              isDragging
                ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                : 'border-slate-300 dark:border-slate-600'
            }`}
          >
            <div className="text-center space-y-6">
              <div className={`inline-flex items-center justify-center w-20 h-20 rounded-2xl ${
                isDragging 
                  ? 'bg-blue-500' 
                  : 'bg-gradient-to-br from-blue-500 to-teal-500'
              }`}>
                <Upload className="w-10 h-10 text-white" />
              </div>

              {!file ? (
                <>
                  <div>
                    <h3 className="text-slate-900 dark:text-white mb-2">
                      Drop your CSV file here
                    </h3>
                    <p className="text-slate-500 dark:text-slate-400">
                      or click to browse from your computer
                    </p>
                  </div>

                  <div>
                    <input
                      type="file"
                      id="file-upload"
                      accept=".csv"
                      onChange={handleFileSelect}
                      className="hidden"
                    />
                    <label htmlFor="file-upload">
                      <Button asChild className="cursor-pointer">
                        <span>Select CSV File</span>
                      </Button>
                    </label>
                  </div>

                  <p className="text-slate-400 dark:text-slate-500">
                    Supported format: CSV (Max 10MB)
                  </p>
                </>
              ) : (
                <div className="space-y-6">
                  <div className="flex items-center justify-center gap-4 p-4 bg-slate-50 dark:bg-slate-700 rounded-xl">
                    <File className="w-8 h-8 text-blue-500" />
                    <div className="flex-1 text-left">
                      <div className="text-slate-900 dark:text-white">{file.name}</div>
                      <p className="text-slate-500 dark:text-slate-400">
                        {(file.size / 1024).toFixed(2)} KB
                      </p>
                    </div>
                    <button
                      onClick={handleReset}
                      className="p-2 hover:bg-slate-200 dark:hover:bg-slate-600 rounded-lg transition-colors"
                    >
                      <X className="w-5 h-5 text-slate-500" />
                    </button>
                  </div>

                  {isUploading && (
                    <div className="space-y-2">
                      <div className="flex justify-between text-slate-600 dark:text-slate-400">
                        <span>Uploading...</span>
                        <span>{uploadProgress}%</span>
                      </div>
                      <Progress value={uploadProgress} />
                    </div>
                  )}

                  {!isUploading && (
                    <Button 
                      onClick={handleUpload}
                      className="bg-gradient-to-r from-blue-500 to-teal-500 hover:from-blue-600 hover:to-teal-600"
                    >
                      Upload File
                    </Button>
                  )}
                </div>
              )}
            </div>
          </div>
        ) : (
          /* Success State */
          <div className="bg-white dark:bg-slate-800 rounded-2xl p-12 border border-slate-200 dark:border-slate-700">
            <div className="text-center space-y-6">
              <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-green-100 dark:bg-green-900/30">
                <CheckCircle2 className="w-10 h-10 text-green-500" />
              </div>
              
              <div>
                <h3 className="text-slate-900 dark:text-white mb-2">Upload Successful!</h3>
                <p className="text-slate-500 dark:text-slate-400">
                  Your CSV file has been processed successfully
                </p>
              </div>

              <div className="flex gap-4 justify-center">
                <Button onClick={handleReset} variant="outline">
                  Upload Another
                </Button>
                <Button 
                  onClick={() => navigate('/visualization')}
                  className="bg-gradient-to-r from-blue-500 to-teal-500 hover:from-blue-600 hover:to-teal-600"
                >
                  View Data
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Quick Preview */}
        {uploadComplete && (
          <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 border border-slate-200 dark:border-slate-700">
            <h3 className="text-slate-900 dark:text-white mb-4">Quick Preview</h3>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-slate-200 dark:border-slate-700">
                    <th className="text-left py-3 px-4 text-slate-600 dark:text-slate-400">Equipment Name</th>
                    <th className="text-left py-3 px-4 text-slate-600 dark:text-slate-400">Type</th>
                    <th className="text-left py-3 px-4 text-slate-600 dark:text-slate-400">Flowrate</th>
                    <th className="text-left py-3 px-4 text-slate-600 dark:text-slate-400">Pressure</th>
                    <th className="text-left py-3 px-4 text-slate-600 dark:text-slate-400">Temperature</th>
                  </tr>
                </thead>
                <tbody>
                  {mockPreviewData.map((row, index) => (
                    <tr key={index} className="border-b border-slate-100 dark:border-slate-700/50">
                      <td className="py-3 px-4 text-slate-900 dark:text-white">{row.name}</td>
                      <td className="py-3 px-4 text-slate-600 dark:text-slate-400">{row.type}</td>
                      <td className="py-3 px-4 text-slate-600 dark:text-slate-400">{row.flowrate}</td>
                      <td className="py-3 px-4 text-slate-600 dark:text-slate-400">{row.pressure}</td>
                      <td className="py-3 px-4 text-slate-600 dark:text-slate-400">{row.temp}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Instructions */}
        <div className="bg-blue-50 dark:bg-blue-900/20 rounded-2xl p-6 border border-blue-200 dark:border-blue-800">
          <h3 className="text-blue-900 dark:text-blue-300 mb-3">CSV Format Requirements</h3>
          <ul className="space-y-2 text-blue-800 dark:text-blue-400">
            <li>• Required columns: Equipment Name, Type, Flowrate, Pressure, Temperature</li>
            <li>• Use comma (,) as delimiter</li>
            <li>• First row should contain column headers</li>
            <li>• Numeric values should not contain units in the CSV</li>
          </ul>
        </div>
      </div>
    </Layout>
  );
}
