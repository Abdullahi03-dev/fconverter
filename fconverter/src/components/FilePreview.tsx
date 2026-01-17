import React, { memo } from 'react';
import { File, X } from 'lucide-react';

interface FilePreviewProps {
    file: File;
    onRemove: () => void;
}

const FilePreview: React.FC<FilePreviewProps> = memo(({ file, onRemove }) => {
    const formatFileSize = (bytes: number): string => {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + ['B', 'KB', 'MB', 'GB'][i];
    };

    return (
        <div className="glass-panel p-4 rounded-xl flex items-center justify-between mt-4">
            <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-lg bg-blue-500/10 flex items-center justify-center text-blue-400 border border-blue-500/20">
                    <File size={24} strokeWidth={1.5} />
                </div>
                <div>
                    <h4 className="font-medium text-white text-sm">{file.name}</h4>
                    <p className="text-xs text-white/40 font-mono mt-0.5">{formatFileSize(file.size)}</p>
                </div>
            </div>
            <button
                onClick={onRemove}
                className="p-2 text-white/40 hover:text-red-400 hover:bg-red-400/10 rounded-lg transition-colors"
            >
                <X size={20} strokeWidth={1.5} />
            </button>
        </div>
    );
});

FilePreview.displayName = 'FilePreview';

export default FilePreview;
