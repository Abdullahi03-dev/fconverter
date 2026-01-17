import React from 'react';
import { Download, CheckCircle, RefreshCw } from 'lucide-react';

interface DownloadSectionProps {
    downloadUrl: string;
    onReset: () => void;
}

const DownloadSection: React.FC<DownloadSectionProps> = ({ downloadUrl, onReset }) => {
    return (
        <div className="mt-8 text-center p-8 glass-panel rounded-2xl border-green-500/20 bg-green-500/5 animate-fade-in-up">
            <div className="w-14 h-14 mx-auto bg-green-500 rounded-full flex items-center justify-center mb-4 shadow-lg shadow-green-500/20">
                <CheckCircle size={28} className="text-white" strokeWidth={2} />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Ready for download</h3>
            <p className="text-white/40 text-sm mb-6">Your document has been successfully converted.</p>

            <div className="flex flex-col sm:flex-row justify-center gap-3">
                <a
                    href={downloadUrl}
                    download
                    className="px-6 py-2.5 bg-white text-black font-semibold rounded-full hover:bg-gray-200 transition-colors shadow-lg shadow-white/10 inline-flex items-center justify-center gap-2"
                >
                    <Download size={18} />
                    Download PDF
                </a>
                <button
                    onClick={onReset}
                    className="px-6 py-2.5 glass-button rounded-full text-white font-medium hover:bg-white/10 inline-flex items-center justify-center gap-2"
                >
                    <RefreshCw size={18} />
                    Convert Another
                </button>
            </div>
        </div>
    );
};

export default DownloadSection;
