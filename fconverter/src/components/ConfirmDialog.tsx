import React from 'react';
import { AlertTriangle, X } from 'lucide-react';

interface ConfirmDialogProps {
    isOpen: boolean;
    title: string;
    message: string;
    onConfirm: () => void;
    onCancel: () => void;
}

const ConfirmDialog: React.FC<ConfirmDialogProps> = ({
    isOpen,
    title,
    message,
    onConfirm,
    onCancel
}) => {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            {/* Backdrop */}
            <div
                className="absolute inset-0 bg-black/80 backdrop-blur-sm"
                onClick={onCancel}
            />

            {/* Dialog */}
            <div className="relative bg-[#0f0f0f] border border-white/10 rounded-2xl p-6 max-w-md w-full shadow-2xl animate-fade-in-up">
                {/* Close button */}
                <button
                    onClick={onCancel}
                    className="absolute top-4 right-4 p-1 text-white/40 hover:text-white/80 transition-colors"
                >
                    <X size={20} />
                </button>

                {/* Icon */}
                <div className="w-12 h-12 rounded-full bg-yellow-500/10 flex items-center justify-center mb-4">
                    <AlertTriangle size={24} className="text-yellow-500" />
                </div>

                {/* Content */}
                <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
                <p className="text-white/60 text-sm mb-6">{message}</p>

                {/* Actions */}
                <div className="flex gap-3">
                    <button
                        onClick={onCancel}
                        className="flex-1 px-4 py-2.5 rounded-lg bg-white/5 border border-white/10 text-white hover:bg-white/10 transition-colors font-medium"
                    >
                        Cancel
                    </button>
                    <button
                        onClick={onConfirm}
                        className="flex-1 px-4 py-2.5 rounded-lg bg-red-600 text-white hover:bg-red-500 transition-colors font-medium"
                    >
                        Continue
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ConfirmDialog;
