import React, { useState, type ChangeEvent, type DragEvent } from 'react';
import { UploadCloud, FileUp, AlertCircle } from 'lucide-react';

interface FileUploadZoneProps {
    onFileSelect: (file: File) => void;
    selectedFile: File | null;
    conversionType: string;
}

const FileUploadZone: React.FC<FileUploadZoneProps> = ({ onFileSelect, selectedFile, conversionType }) => {
    const [isDragging, setIsDragging] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Define accepted file types based on conversion type
    const getAcceptedTypes = () => {
        switch (conversionType) {
            case 'image_to_pdf':
                return {
                    accept: 'image/*',
                    extensions: ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
                    label: 'Images (JPG, PNG, GIF, BMP, TIFF)'
                };
            case 'docx_to_pdf':
                return {
                    accept: '.docx',
                    extensions: ['.docx'],
                    label: 'Word Documents (.docx)'
                };
            case 'text_to_pdf':
                return {
                    accept: '.txt',
                    extensions: ['.txt'],
                    label: 'Text Files (.txt)'
                };
            default:
                return {
                    accept: '*',
                    extensions: [],
                    label: 'All Files'
                };
        }
    };

    const validateFile = (file: File): boolean => {
        setError(null);

        // Check file size (10MB limit)
        const maxSize = 10 * 1024 * 1024; // 10MB in bytes
        if (file.size > maxSize) {
            setError('File size exceeds 10MB limit');
            return false;
        }

        // Check file type
        const accepted = getAcceptedTypes();
        const fileName = file.name.toLowerCase();
        const isValidType = accepted.extensions.some(ext => fileName.endsWith(ext));

        if (!isValidType && accepted.extensions.length > 0) {
            setError(`Invalid file type. Please select ${accepted.label}`);
            return false;
        }

        return true;
    };

    const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = () => setIsDragging(false);

    const handleDrop = (e: DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        setIsDragging(false);
        const file = e.dataTransfer.files[0];
        if (file && validateFile(file)) {
            onFileSelect(file);
        }
    };

    const handleFileInput = (e: ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file && validateFile(file)) {
            onFileSelect(file);
        }
    };

    if (selectedFile) return null;

    const accepted = getAcceptedTypes();

    return (
        <div>
            <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={`glass-panel rounded-2xl p-10 text-center transition-all duration-300 border-dashed border-2 group ${isDragging
                        ? 'border-blue-500 bg-blue-500/5'
                        : error
                            ? 'border-red-500/50 bg-red-500/5'
                            : 'border-white/10 hover:border-white/20'
                    }`}
            >
                <div className="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center mx-auto mb-6 ring-1 ring-white/10 group-hover:scale-110 transition-transform duration-300">
                    <UploadCloud size={32} className="text-white/80" strokeWidth={1.5} />
                </div>

                <h3 className="text-xl font-medium text-white mb-2">Upload your file</h3>
                <p className="text-white/40 text-sm mb-6">Drag and drop or click to browse</p>

                <label className="inline-block relative">
                    <input
                        type="file"
                        onChange={handleFileInput}
                        className="hidden"
                        accept={accepted.accept}
                    />
                    <span className="glass-button px-6 py-2.5 rounded-full text-sm font-medium text-white cursor-pointer inline-flex items-center gap-2 hover:bg-white/10 transition-colors">
                        <FileUp size={16} />
                        Select File
                    </span>
                </label>

                <p className="mt-4 text-[10px] text-white/20 uppercase tracking-widest font-mono">
                    {accepted.label}
                </p>
            </div>

            {error && (
                <div className="mt-3 p-3 rounded-lg bg-red-500/10 border border-red-500/20 flex items-center gap-2 text-red-400 text-sm">
                    <AlertCircle size={16} />
                    <span>{error}</span>
                </div>
            )}
        </div>
    );
};

export default FileUploadZone;
