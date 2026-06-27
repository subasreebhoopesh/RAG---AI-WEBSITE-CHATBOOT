import { NavLink } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Home, 
  Globe, 
  MessageSquare, 
  Menu, 
  X,
  Bot
} from 'lucide-react';
import { useState } from 'react';

const Sidebar = ({ isOpen, onClose, isMobile }) => {
  const navItems = [
    { path: '/', icon: Home, label: 'Home' },
    { path: '/index', icon: Globe, label: 'Index Website' },
    { path: '/chat', icon: MessageSquare, label: 'Ask Questions' },
  ];

  return (
    <>
      {/* Mobile overlay */}
      <AnimatePresence>
        {isMobile && isOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <motion.aside
        initial={isMobile ? { x: '-100%' } : false}
        animate={{ x: isOpen ? 0 : isMobile ? '-100%' : 0 }}
        transition={{ type: 'spring', damping: 25, stiffness: 200 }}
        className={`
          fixed left-0 top-0 h-full w-64 glass z-50
          ${isMobile ? 'lg:hidden' : 'hidden lg:block'}
        `}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="p-6 border-b border-slate-200 dark:border-slate-700">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center">
                <Bot className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
                  CrawlAI RAG
                </h1>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  AI-Powered Intelligence
                </p>
              </div>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-2">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={isMobile ? onClose : undefined}
                className={({ isActive }) => `
                  flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200
                  ${isActive 
                    ? 'bg-gradient-to-r from-primary-500 to-primary-600 text-white shadow-lg shadow-primary-500/30' 
                    : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
                  }
                `}
              >
                <item.icon className="w-5 h-5" />
                <span className="font-medium">{item.label}</span>
              </NavLink>
            ))}
          </nav>

          {/* Footer */}
          <div className="p-4 border-t border-slate-200 dark:border-slate-700">
            <p className="text-xs text-slate-500 dark:text-slate-400 text-center">
              Built with React + Tailwind
            </p>
          </div>
        </div>
      </motion.aside>
    </>
  );
};

export default Sidebar;
