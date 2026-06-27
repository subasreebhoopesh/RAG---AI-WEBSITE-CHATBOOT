import { forwardRef } from 'react';

const Input = forwardRef(({ 
  label, 
  error, 
  icon: Icon, 
  className = '', 
  ...props 
}, ref) => {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
          {label}
        </label>
      )}
      <div className="relative">
        {Icon && (
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Icon className="h-5 w-5 text-slate-400" />
          </div>
        )}
        <input
          ref={ref}
          className={`
            w-full px-4 py-3
            ${Icon ? 'pl-11' : ''}
            rounded-xl border-2
            ${error ? 'border-red-500 focus:border-red-500' : 'border-slate-200 dark:border-slate-700 focus:border-primary-500'}
            bg-white/50 dark:bg-slate-800/50
            text-slate-900 dark:text-slate-100
            placeholder-slate-400 dark:placeholder-slate-500
            focus:outline-none focus:ring-2 focus:ring-primary-500/20
            transition-all duration-200
            ${className}
          `}
          {...props}
        />
      </div>
      {error && (
        <p className="mt-1 text-sm text-red-500">{error}</p>
      )}
    </div>
  );
});

Input.displayName = 'Input';

export default Input;
