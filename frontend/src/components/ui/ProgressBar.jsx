import { motion } from 'framer-motion';

const ProgressBar = ({ progress, status }) => {
  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
          {status}
        </span>
        <span className="text-sm font-semibold text-primary-600 dark:text-primary-400">
          {progress.toFixed(1)}%
        </span>
      </div>
      <div className="w-full h-3 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          transition={{ duration: 0.3 }}
          className="h-full bg-gradient-to-r from-primary-500 to-primary-600 rounded-full"
        />
      </div>
    </div>
  );
};

export default ProgressBar;
