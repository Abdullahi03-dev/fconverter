import React, { memo } from 'react';

interface ConversionProgressProps {
    progress: number;
}

const ConversionProgress: React.FC<ConversionProgressProps> = memo(({ progress }) => {
    return (
        <div className="mt-8">
            <div className="flex justify-between text-xs font-medium mb-2">
                <span className="text-white/80">Processing file...</span>
                <span className="text-blue-400">{progress}%</span>
            </div>
            <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                <div
                    className="h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-300 ease-out will-change-[width]"
                    style={{ width: `${progress}%` }}
                />
            </div>
        </div>
    );
});

ConversionProgress.displayName = 'ConversionProgress';

export default ConversionProgress;
