import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import { Upload, File, CheckCircle2, X } from 'lucide-react';
import { api } from '../api/client';

export default function UploadPage({ onLogout }) {
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadComplete, setUploadComplete] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.name.endsWith('.csv')) {
      setFile(droppedFile);
      setError(null);
    } else {
      setError('Please upload a CSV file');
    }
  };

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files?.[0];
    console.log('File selected:', selectedFile);
    if (selectedFile) {
      if (selectedFile.name.endsWith('.csv')) {
        setFile(selectedFile);
        setError(null);
        console.log('CSV file accepted:', selectedFile.name);
      } else {
        setError('Please upload a CSV file');
        console.error('Invalid file type:', selectedFile.name);
      }
    }
  };

  const handleUpload = async () => {
    if (!file) {
      console.error('No file selected');
      setError('Please select a file first');
      return;
    }

    console.log('Starting upload for file:', file.name);
    setIsUploading(true);
    setUploadProgress(0);
    setError(null);

    try {
      // Ensure CSRF token is available before upload
      await api.getCsrfToken();
      
      // Simulate progress
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      console.log('Calling API to upload file...');
      const response = await api.uploadCSV(file);
      console.log('Upload successful:', response.data);
      
      clearInterval(progressInterval);
      setUploadProgress(100);
      setUploadResult(response.data);
      setUploadComplete(true);
    } catch (error) {
      console.error('Upload error:', error);
      const errorMessage = error.response?.data?.error || 
                          error.response?.data?.message || 
                          error.response?.data?.detail ||
                          error.message || 
                          'Upload failed. Please check if the backend is running.';
      setError(errorMessage);
      setUploadProgress(0);
    } finally {
      setIsUploading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setUploadComplete(false);
    setUploadProgress(0);
    setUploadResult(null);
    setError(null);
  };

  return (
    <Layout onLogout={onLogout}>
      <div className="max-w-4xl mx-auto space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white mb-2">Upload CSV Data</h1>
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
            onClick={() => {
              if (!file) {
                document.getElementById('file-upload')?.click();
              }
            }}
            className={`bg-white dark:bg-slate-800 rounded-2xl p-12 border-2 border-dashed transition-all ${
              isDragging
                ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                : 'border-slate-300 dark:border-slate-600'
            } ${!file ? 'cursor-pointer' : ''}`}
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
                    <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">
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
                    <label 
                      htmlFor="file-upload"
                      className="inline-block px-6 py-3 rounded-xl bg-gradient-to-r from-blue-500 to-teal-500 hover:from-blue-600 hover:to-teal-600 text-white font-semibold cursor-pointer transition-all"
                    >
                      Select CSV File
                    </label>
                  </div>

                  <p className="text-slate-400 dark:text-slate-500 text-sm">
                    Supported format: CSV (Max 10MB)
                  </p>
                </>
              ) : (
                <div className="space-y-6">
                  <div className="flex items-center justify-center gap-4 p-4 bg-slate-50 dark:bg-slate-700 rounded-xl">
                    <File className="w-8 h-8 text-blue-500" />
                    <div className="flex-1 text-left">
                      <div className="text-slate-900 dark:text-white font-medium">{file.name}</div>
                      <p className="text-slate-500 dark:text-slate-400 text-sm">
                        {(file.size / 1024).toFixed(2)} KB
                      </p>
                    </div>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleReset();
                      }}
                      className="p-2 hover:bg-slate-200 dark:hover:bg-slate-600 rounded-lg transition-colors cursor-pointer"
                    >
                      <X className="w-5 h-5 text-slate-500" />
                    </button>
                  </div>

                  {isUploading && (
                    <div className="space-y-2">
                      <div className="flex justify-between text-slate-600 dark:text-slate-400 text-sm">
                        <span>Uploading...</span>
                        <span>{uploadProgress}%</span>
                      </div>
                      <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2">
                        <div
                          className="bg-gradient-to-r from-blue-500 to-teal-500 h-2 rounded-full transition-all"
                          style={{ width: `${uploadProgress}%` }}
                        />
                      </div>
                    </div>
                  )}

                  {!isUploading && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleUpload();
                      }}
                      className="px-6 py-3 rounded-xl bg-gradient-to-r from-blue-500 to-teal-500 hover:from-blue-600 hover:to-teal-600 text-white font-semibold transition-all cursor-pointer"
                    >
                      Upload File
                    </button>
                  )}

                  {error && (
                    <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl">
                      <p className="text-red-600 dark:text-red-400 text-sm">{error}</p>
                    </div>
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
                <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">Upload Successful!</h3>
                <p className="text-slate-500 dark:text-slate-400">
                  Your CSV file has been processed successfully
                </p>
                {uploadResult && (
                  <div className="mt-4 p-4 bg-slate-50 dark:bg-slate-700 rounded-xl text-left">
                    <p className="text-sm text-slate-600 dark:text-slate-400">
                      <strong>Created:</strong> {uploadResult.created_count} records<br />
                      <strong>Updated:</strong> {uploadResult.updated_count} records<br />
                      <strong>Total:</strong> {uploadResult.total_records} records
                    </p>
                  </div>
                )}
              </div>

              <div className="flex gap-4 justify-center">
                <button
                  onClick={handleReset}
                  className="px-6 py-3 rounded-xl border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 transition-all"
                >
                  Upload Another
                </button>
                <button
                  onClick={() => navigate('/visualization')}
                  className="px-6 py-3 rounded-xl bg-gradient-to-r from-blue-500 to-teal-500 hover:from-blue-600 hover:to-teal-600 text-white font-semibold transition-all"
                >
                  View Data
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Instructions */}
        <div className="bg-blue-50 dark:bg-blue-900/20 rounded-2xl p-6 border border-blue-200 dark:border-blue-800">
          <h3 className="text-blue-900 dark:text-blue-300 mb-3 font-semibold">CSV Format Requirements</h3>
          <ul className="space-y-2 text-blue-800 dark:text-blue-400 text-sm">
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

