import React, { memo } from 'react';
import { Image as ImageIcon, FileText, Type } from 'lucide-react';

interface ConversionTypeSelectorProps {
    selected: string;
    onChange: (id: string) => void;
}

const ConversionTypeSelector: React.FC<ConversionTypeSelectorProps> = memo(({ selected, onChange }) => {
    const types = [
        { id: 'image_to_pdf', name: 'Image to PDF', icon: ImageIcon },
        { id: 'docx_to_pdf', name: 'Word to PDF', icon: FileText },
        { id: 'text_to_pdf', name: 'Text to PDF', icon: Type },
    ];

    return (
        <div className="mb-8">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {types.map((type) => (
                    <button
                        key={type.id}
                        onClick={() => onChange(type.id)}
                        className={`p-4 rounded-xl flex items-center justify-center gap-3 transition-all duration-200 border ${selected === type.id
                                ? 'bg-blue-500/10 border-blue-500/50 text-white'
                                : 'bg-white/5 border-white/5 text-white/60 hover:bg-white/10 hover:border-white/10 hover:text-white'
                            }`}
                    >
                        <type.icon size={20} strokeWidth={1.5} />
                        <span className="font-medium text-sm">{type.name}</span>
                    </button>
                ))}
            </div>
        </div>
    );
});

ConversionTypeSelector.displayName = 'ConversionTypeSelector';

export default ConversionTypeSelector;
