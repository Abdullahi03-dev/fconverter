import React from 'react';

const Footer: React.FC = () => {
    return (
        <footer className="py-8 mt-auto border-t border-white/5">
            <div className="container mx-auto px-6 flex justify-between items-center text-xs text-white/40">
                <p>&copy; {new Date().getFullYear()} fconverter AI. All rights reserved.</p>
                <div className="flex gap-4">
                    <a href="#" className="hover:text-white/80 transition-colors">Privacy</a>
                    <a href="#" className="hover:text-white/80 transition-colors">Terms</a>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
