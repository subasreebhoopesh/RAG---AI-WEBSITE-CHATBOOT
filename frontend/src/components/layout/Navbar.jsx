import { Menu } from 'lucide-react';
import { motion } from 'framer-motion';

const Navbar = ({ onMenuClick, isMobile }) => {
  return (
    <motion.nav
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="glass-card sticky top-0 z-30 px-6 py-4"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          {isMobile && (
            <button
              onClick={onMenuClick}
              className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            >
              <Menu className="w-6 h-6 text-slate-600 dark:text-slate-300" />
            </button>
          )}
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center">
              <span className="text-white font-bold text-sm">AI</span>
            </div>
            <span className="font-semibold text-slate-800 dark:text-slate-200 hidden sm:block">
              CrawlAI RAG
            </span>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 text-sm">
            <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
            <span>Backend Connected</span>
          </div>
        </div>
      </div>
    </motion.nav>
  );
};

export default Navbar;
