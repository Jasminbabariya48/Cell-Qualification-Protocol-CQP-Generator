import { useState } from 'react';
import axios from 'axios';
import { Upload, FileText, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';

function App() {
  const [files, setFiles] = useState({ tmp: null, acl: null, datasheet: null });
  const [market, setMarket] = useState('EU / UN-38.3 US / DOT Global');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleFileChange = (type) => (e) => {
    setFiles(prev => ({ ...prev, [type]: e.target.files[0] }));
  };

  const handleGenerate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    const formData = new FormData();
    formData.append('tmp_file', files.tmp);
    formData.append('acl_file', files.acl);
    formData.append('datasheet_file', files.datasheet);
    formData.append('market', market);

    try {
      const response = await axios.post('/generate', formData, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'CQP_Generated.docx');
      document.body.appendChild(link);
      link.click();
      link.remove();
      setSuccess(true);
    } catch (err) {
      if (err.response && err.response.data instanceof Blob) {
        const text = await err.response.data.text();
        setError("Generation failed: " + text);
      } else {
        setError("Network error: " + err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden md:max-w-2xl p-8">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-extrabold text-gray-900 flex items-center justify-center gap-3">
            <FileText className="h-8 w-8 text-blue-600" />
            CQP Generator
          </h2>
          <p className="mt-2 text-sm text-gray-600">Dynamic Cell Qualification Protocol Builder</p>
        </div>

        <form onSubmit={handleGenerate} className="space-y-6">
          {['tmp', 'acl', 'datasheet'].map((type) => (
            <div key={type} className="space-y-1">
              <label className="block text-sm font-medium text-gray-700 capitalize">
                {type === 'tmp' ? 'Test Method Procedure (.docx)' : 
                 type === 'acl' ? 'Acceptance Criteria (.docx)' : 'Vendor Datasheet (.pdf)'}
              </label>
              <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md hover:border-blue-500 transition-colors">
                <div className="space-y-1 text-center">
                  <Upload className="mx-auto h-12 w-12 text-gray-400" />
                  <div className="flex text-sm text-gray-600">
                    <label className="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500">
                      <span>Upload a file</span>
                      <input type="file" className="sr-only" required accept={type === 'datasheet' ? '.pdf' : '.docx'} onChange={handleFileChange(type)} />
                    </label>
                  </div>
                  <p className="text-xs text-gray-500">{files[type] ? files[type].name : 'No file selected'}</p>
                </div>
              </div>
            </div>
          ))}

          <div>
            <label className="block text-sm font-medium text-gray-700">Target Market</label>
            <input type="text" value={market} onChange={e => setMarket(e.target.value)} className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md p-2 border" />
          </div>

          <button type="submit" disabled={loading} className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50">
            {loading ? <><Loader2 className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" /> Generating...</> : 'Generate Protocol'}
          </button>
        </form>

        {error && (
          <div className="mt-4 rounded-md bg-red-50 p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <AlertCircle className="h-5 w-5 text-red-400" aria-hidden="true" />
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <div className="mt-2 text-sm text-red-700 whitespace-pre-wrap">{error}</div>
              </div>
            </div>
          </div>
        )}

        {success && (
          <div className="mt-4 rounded-md bg-green-50 p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <CheckCircle className="h-5 w-5 text-green-400" aria-hidden="true" />
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-green-800">Success</h3>
                <div className="mt-2 text-sm text-green-700">Protocol generated and downloaded successfully.</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
