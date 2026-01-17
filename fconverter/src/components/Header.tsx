import React from 'react';
import { Zap } from 'lucide-react';

const Header: React.FC = () => {
    return (
        <header className="fixed top-0 w-full z-50 border-b border-white/5 bg-black/50 backdrop-blur-xl">
            <div className="container mx-auto px-6 h-16 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-600 to-purple-600 flex items-center justify-center text-white shadow-lg shadow-blue-500/20">
                        <Zap size={18} fill="currentColor" className="text-white" />
                    </div>
                    <span className="font-bold text-lg tracking-tight text-white">
                        fconverter
                    </span>
                </div>

                {/* <nav className="flex gap-6 text-sm font-medium text-white/60">
                    <a href="#" className="hover:text-white transition-colors">Documentation</a>
                    <a href="#" className="hover:text-white transition-colors">API</a>
                    <button className="bg-white text-black px-4 py-1.5 rounded-full hover:bg-gray-200 transition-colors font-semibold text-xs">
                        Start Free
                    </button>
                </nav> */}
            </div>
        </header>
    );
};

export default Header;
