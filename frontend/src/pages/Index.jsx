import { useState } from 'react';
import { motion } from 'framer-motion';
import { Globe, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import Card from '../components/ui/Card';
import ProgressBar from '../components/ui/ProgressBar';
import { apiService } from '../services/api';

const Index = () => {
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');
  const [isIndexing, setIsIndexing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState('');
  const [result, setResult] = useState(null);

  const stages = [
    { progress: 5, status: '🚀 Launching headless browser...' },
    { progress: 15, status: '🌐 Rendering website with JavaScript...' },
    { progress: 28, status: '🔍 Crawling internal pages...' },
    { progress: 42, status: '📄 Extracting visible content...' },
    { progress: 55, status: '✂️ Chunking text content...' },
    { progress: 68, status: '🧠 Generating embeddings...' },
    { progress: 75, status: '💾 Saving to vector store...' },
    { progress: 82, status: '🔗 Indexing chunks...' },
    { progress: 88, status: '⚡ Finalizing index...' },
    { progress: 93, status: '🔄 Almost done...' },
    { progress: 97, status: '⏳ Processing, please wait...' },
  ];

  const validateUrl = (url) => {
    if (!url) {
      return 'Please enter a website URL';
    }
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      return 'Invalid URL! Must start with http:// or https://';
    }
    if (url.includes('google.com/search')) {
      return 'Google Search URLs cannot be crawled!';
    }
    return '';
  };

  const handleIndex = async (e) => {
    e.preventDefault();
    
    const validationError = validateUrl(url);
    if (validationError) {
      setError(validationError);
      return;
    }

    setError('');
    setIsIndexing(true);
    setProgress(0);
    setStatus('Starting...');
    setResult(null);

    // Simulate progress stages
    let currentStage = 0;
    const progressInterval = setInterval(() => {
      if (currentStage < stages.length) {
        setProgress(stages[currentStage].progress);
        setStatus(stages[currentStage].status);
        currentStage++;
      } else {
        clearInterval(progressInterval);
      }
    }, 800);

    try {
      const response = await apiService.ingestWebsite(url);
      clearInterval(progressInterval);
      setProgress(100);
      setStatus('✅ Indexing complete!');
      setResult(response);
    } catch (err) {
      clearInterval(progressInterval);
      setError(err.message);
      setProgress(0);
    } finally {
      setIsIndexing(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-3xl md:text-4xl font-bold mb-2 text-slate-800 dark:text-slate-200">
          Index a Website
        </h1>
        <p className="text-slate-600 dark:text-slate-400">
          Enter a website URL to crawl, index, and make it queryable
        </p>
      </motion.div>

      <Card className="mb-8">
        <form onSubmit={handleIndex} className="space-y-6">
          <Input
            label="Website URL"
            icon={Globe}
            placeholder="https://example.com"
            value={url}
            onChange={(e) => {
              setUrl(e.target.value);
              setError('');
            }}
            error={error}
            disabled={isIndexing}
          />

          <Button
            type="submit"
            loading={isIndexing}
            disabled={isIndexing}
            className="w-full"
            size="lg"
          >
            {isIndexing ? 'Indexing...' : 'Index Website'}
          </Button>
        </form>
      </Card>

      {isIndexing && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <Card>
            <div className="flex items-center gap-3 mb-4">
              <Loader2 className="w-6 h-6 text-primary-600 animate-spin" />
              <span className="font-semibold text-slate-800 dark:text-slate-200">
                Indexing in Progress
              </span>
            </div>
            <ProgressBar progress={progress} status={status} />
          </Card>
        </motion.div>
      )}

      {result && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <Card className="border-l-4 border-l-green-500">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center flex-shrink-0">
                <CheckCircle className="w-6 h-6 text-green-600 dark:text-green-400" />
              </div>
              <div className="flex-1">
                <h3 className="text-xl font-semibold mb-2 text-slate-800 dark:text-slate-200">
                  Website Indexed Successfully!
                </h3>
                <div className="space-y-2 text-slate-600 dark:text-slate-400">
                  <p><strong>Pages Scraped:</strong> {result.pages_scraped}</p>
                  <p><strong>Chunks Created:</strong> {result.chunks_created}</p>
                  <p><strong>Status:</strong> {result.status}</p>
                </div>
                <p className="mt-4 text-sm text-slate-500 dark:text-slate-400">
                  You can now ask questions about this website in the Chat section.
                </p>
              </div>
            </div>
          </Card>
        </motion.div>
      )}

      {error && !isIndexing && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <Card className="border-l-4 border-l-red-500 bg-red-50 dark:bg-red-900/10">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center flex-shrink-0">
                <AlertCircle className="w-6 h-6 text-red-600 dark:text-red-400" />
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-2 text-red-800 dark:text-red-200">
                  Indexing Failed
                </h3>
                <p className="text-red-600 dark:text-red-400">{error}</p>
              </div>
            </div>
          </Card>
        </motion.div>
      )}

      <Card className="bg-slate-50 dark:bg-slate-800/50">
        <h3 className="font-semibold mb-3 text-slate-800 dark:text-slate-200">
          Tips for Better Results
        </h3>
        <ul className="space-y-2 text-sm text-slate-600 dark:text-slate-400">
          <li>• Use direct website URLs (not search results)</li>
          <li>• Ensure the website is publicly accessible</li>
          <li>• Some websites may block crawlers</li>
          <li>• Large websites may take longer to index</li>
        </ul>
      </Card>
    </div>
  );
};

export default Index;
