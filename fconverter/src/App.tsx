import { useState, useCallback } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import ConversionTypeSelector from './components/ConversionTypeSelector';
import FileUploadZone from './components/FileUploadZone';
import FilePreview from './components/FilePreview';
import ConversionProgress from './components/ConversionProgress';
import DownloadSection from './components/DownloadSection';
import ConfirmDialog from './components/ConfirmDialog';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [conversionType, setConversionType] = useState('image_to_pdf');
  const [isConverting, setIsConverting] = useState(false);
  const [progress, setProgress] = useState(0);
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Confirmation dialog state
  const [showConfirmDialog, setShowConfirmDialog] = useState(false);
  const [pendingConversionType, setPendingConversionType] = useState<string | null>(null);

  const handleReset = useCallback(() => {
    setSelectedFile(null);
    setDownloadUrl(null);
    setProgress(0);
    setError(null);
    setIsConverting(false);
  }, []);

  const handleFileSelect = useCallback((file: File) => {
    setSelectedFile(file);
    setDownloadUrl(null);
    setError(null);
    setProgress(0);
  }, []);

  const handleConversionTypeChange = useCallback((newType: string) => {
    // If user has selected a file or has a download ready, warn them
    if (selectedFile || downloadUrl) {
      setPendingConversionType(newType);
      setShowConfirmDialog(true);
    } else {
      setConversionType(newType);
    }
  }, [selectedFile, downloadUrl]);

  const handleConfirmSwitch = useCallback(() => {
    if (pendingConversionType) {
      handleReset();
      setConversionType(pendingConversionType);
      setPendingConversionType(null);
    }
    setShowConfirmDialog(false);
  }, [pendingConversionType, handleReset]);

  const handleCancelSwitch = useCallback(() => {
    setPendingConversionType(null);
    setShowConfirmDialog(false);
  }, []);

  const handleConvert = useCallback(async () => {
    if (!selectedFile) return;

    setIsConverting(true);
    setProgress(0);
    setError(null);

    try {
      // Create FormData for file upload
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('conversion_type', conversionType);

      // Simulate progress during upload
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      // Make API call
      const response = await fetch(`${API_BASE_URL}/api/v1/convert`, {
        method: 'POST',
        body: formData,
      });

      clearInterval(progressInterval);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Conversion failed');
      }

      const result = await response.json();

      // Complete progress
      setProgress(100);

      // Set download URL
      const fullDownloadUrl = `${API_BASE_URL}${result.download_url}`;
      setDownloadUrl(fullDownloadUrl);

    } catch (err) {
      console.error('Conversion error:', err);
      setError(err instanceof Error ? err.message : 'An error occurred during conversion');
      setProgress(0);
    } finally {
      setIsConverting(false);
    }
  }, [selectedFile, conversionType]);

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <main className="flex-grow pt-32 pb-12 px-4">
        <div className="max-w-xl mx-auto">
          {/* Header Text */}
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-white mb-4 tracking-tight">
              Transform your <span className="gradient-text">files</span>
            </h1>
            <p className="text-lg text-white/50 max-w-sm mx-auto">
              Professional grade file conversion powered by advanced AI processing.
            </p>
          </div>

          {/* Main Interface */}
          <div className="relative">
            <div className="relative bg-[#0A0A0A] rounded-2xl border border-white/10 p-1 shadow-2xl">
              <div className="bg-[#0f0f0f] rounded-xl p-8 border border-white/5">

                <ConversionTypeSelector
                  selected={conversionType}
                  onChange={handleConversionTypeChange}
                />

                <FileUploadZone
                  onFileSelect={handleFileSelect}
                  selectedFile={selectedFile}
                  conversionType={conversionType}
                />

                {selectedFile && !isConverting && !downloadUrl && (
                  <FilePreview file={selectedFile} onRemove={handleReset} />
                )}

                {isConverting && <ConversionProgress progress={progress} />}

                {downloadUrl && <DownloadSection downloadUrl={downloadUrl} onReset={handleReset} />}

                {error && (
                  <div className="mt-6 p-4 bg-red-500/10 border border-red-500/20 rounded-xl">
                    <p className="text-red-400 text-sm text-center">{error}</p>
                  </div>
                )}

                {selectedFile && !isConverting && !downloadUrl && (
                  <button
                    onClick={handleConvert}
                    disabled={isConverting}
                    className="w-full mt-6 bg-white text-black font-bold h-12 rounded-xl hover:bg-gray-200 transition-all transform active:scale-[0.99] shadow-lg shadow-white/5 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Convert File
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>

      <Footer />

      {/* Confirmation Dialog */}
      <ConfirmDialog
        isOpen={showConfirmDialog}
        title="Switch Conversion Type?"
        message="Switching conversion type will clear your current file and progress. Are you sure you want to continue?"
        onConfirm={handleConfirmSwitch}
        onCancel={handleCancelSwitch}
      />
    </div>
  );
}

export default App;
