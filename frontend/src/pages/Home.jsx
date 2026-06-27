import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { ArrowRight, Globe, MessageSquare, Sparkles, Zap, Shield } from 'lucide-react';
import Card from '../components/ui/Card';

const Home = () => {
  const features = [
    {
      icon: Globe,
      title: 'Website Crawling',
      description: 'Crawl entire websites and extract clean, readable content automatically.',
    },
    {
      icon: Sparkles,
      title: 'AI-Powered Indexing',
      description: 'Advanced RAG technology transforms websites into queryable knowledge bases.',
    },
    {
      icon: MessageSquare,
      title: 'Natural Q&A',
      description: 'Ask questions in natural language and get accurate, grounded answers.',
    },
    {
      icon: Zap,
      title: 'Lightning Fast',
      description: 'Built with FastAPI and ChromaDB for optimal performance.',
    },
    {
      icon: Shield,
      title: 'Secure & Private',
      description: 'Your data stays secure with environment-based configuration.',
    },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center mb-16"
      >
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 text-sm font-medium mb-6">
          <Sparkles className="w-4 h-4" />
          <span>AI-Powered Website Intelligence</span>
        </div>
        
        <h1 className="text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-primary-600 via-secondary-600 to-primary-600 bg-clip-text text-transparent">
          CrawlAI RAG
        </h1>
        
        <p className="text-xl text-slate-600 dark:text-slate-400 mb-8 max-w-2xl mx-auto">
          Transform any website into an intelligent knowledge base. Crawl, index, and ask questions with the power of AI.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link to="/index">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-8 py-4 bg-gradient-to-r from-primary-600 to-primary-500 text-white rounded-xl font-semibold shadow-lg shadow-primary-500/30 flex items-center justify-center gap-2"
            >
              <Globe className="w-5 h-5" />
              Start Indexing
              <ArrowRight className="w-5 h-5" />
            </motion.button>
          </Link>
          <Link to="/chat">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-8 py-4 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 rounded-xl font-semibold border-2 border-slate-200 dark:border-slate-700 flex items-center justify-center gap-2"
            >
              <MessageSquare className="w-5 h-5" />
              Ask Questions
            </motion.button>
          </Link>
        </div>
      </motion.div>

      {/* Features Grid */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3, duration: 0.6 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
      >
        {features.map((feature, index) => (
          <motion.div
            key={feature.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 * index }}
          >
            <Card hover className="h-full">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center mb-4">
                <feature.icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-semibold mb-2 text-slate-800 dark:text-slate-200">
                {feature.title}
              </h3>
              <p className="text-slate-600 dark:text-slate-400">
                {feature.description}
              </p>
            </Card>
          </motion.div>
        ))}
      </motion.div>

      {/* How It Works */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5, duration: 0.6 }}
        className="mt-16"
      >
        <h2 className="text-3xl font-bold text-center mb-8 text-slate-800 dark:text-slate-200">
          How It Works
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            { step: '1', title: 'Index Website', desc: 'Enter a URL and let our AI crawl the entire website' },
            { step: '2', title: 'Process Content', desc: 'Content is chunked, embedded, and stored in vector database' },
            { step: '3', title: 'Ask Questions', desc: 'Query the knowledge base with natural language' },
          ].map((item) => (
            <div key={item.step} className="text-center">
              <div className="w-16 h-16 rounded-full bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center mx-auto mb-4 text-white text-2xl font-bold">
                {item.step}
              </div>
              <h3 className="text-lg font-semibold mb-2 text-slate-800 dark:text-slate-200">
                {item.title}
              </h3>
              <p className="text-slate-600 dark:text-slate-400">
                {item.desc}
              </p>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

export default Home;
