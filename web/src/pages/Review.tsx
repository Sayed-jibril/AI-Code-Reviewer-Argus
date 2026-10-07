import React, { useState } from 'react';
import { reviewFiles } from '../api';
import { ReviewResult, Issue } from '../api';
import IssueCard from '../components/IssueCard';

const Review: React.FC = () => {
  const [files, setFiles] = useState<File[]>([]);
  const [result, setResult] = useState<ReviewResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [severityFilter, setSeverityFilter] = useState<string>('all');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files));
      setError(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (files.length === 0) {
      setError('Please select at least one file');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await reviewFiles(files);
      setResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const filteredIssues = result?.issues.filter(issue => 
    severityFilter === 'all' || issue.severity === severityFilter
  ) || [];

  const getSeverityCount = (severity: string) => {
    return result?.issues.filter(issue => issue.severity === severity).length || 0;
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* File Upload Section */}
      <div className="card mb-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="files" className="block text-lg font-semibold text-text-primary mb-4">
              Upload Code Files
            </label>
            <div className="border-2 border-dashed border-border-color rounded-lg p-8 text-center hover:border-accent-primary transition-colors">
              <input
                type="file"
                id="files"
                multiple
                onChange={handleFileChange}
                className="hidden"
                accept=".py,.js,.ts,.jsx,.tsx,.java,.cs,.c,.cpp,.h,.hpp,.go,.rs,.php,.rb,.swift,.kt,.scala,.dart,.lua,.pl,.r,.sh,.sql,.vb,.hs,.ml,.fs,.ex,.erl,.clj,.f,.cob,.pas,.adb,.sol,.vhd,.sv,.tcl,.hx,.elm,.cu,.cl,.asm,.s"
              />
              <label htmlFor="files" className="cursor-pointer">
                <div className="space-y-4">
                  <svg className="mx-auto h-12 w-12 text-text-muted" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                    <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                  <div>
                    <p className="text-lg text-text-primary">
                      <span className="text-accent-primary font-semibold">Click to upload</span> or drag and drop
                    </p>
                    <p className="text-text-secondary">Support for 41+ programming languages</p>
                  </div>
                </div>
              </label>
            </div>
          </div>

          {files.length > 0 && (
            <div>
              <h3 className="text-lg font-semibold text-text-primary mb-3">Selected Files:</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {files.map((file, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-tertiary-bg rounded-lg">
                    <span className="text-text-secondary text-sm truncate">{file.name}</span>
                    <button
                      type="button"
                      onClick={() => setFiles(files.filter((_, i) => i !== index))}
                      className="text-accent-error hover:text-red-400 ml-2"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {error && (
            <div className="p-4 bg-red-900/20 border border-accent-error rounded-lg text-accent-error">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading || files.length === 0}
            className="btn btn-primary w-full md:w-auto disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing...
              </>
            ) : (
              <>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Analyze Code
              </>
            )}
          </button>
        </form>
      </div>

      {/* Results Section */}
      {result && (
        <div className="space-y-8">
          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="card text-center">
              <div className="text-3xl font-bold text-accent-primary">{result.metrics.files}</div>
              <div className="text-text-secondary">Files Analyzed</div>
            </div>
            <div className="card text-center">
              <div className="text-3xl font-bold text-accent-info">{result.metrics.functions}</div>
              <div className="text-text-secondary">Functions Found</div>
            </div>
            <div className="card text-center">
              <div className="text-3xl font-bold text-accent-warning">{result.metrics.avgComplexity.toFixed(1)}</div>
              <div className="text-text-secondary">Avg Complexity</div>
            </div>
            <div className="card text-center">
              <div className="text-3xl font-bold text-accent-error">{result.issues.length}</div>
              <div className="text-text-secondary">Issues Found</div>
            </div>
          </div>

          {/* Severity Filter */}
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setSeverityFilter('all')}
              className={`btn ${severityFilter === 'all' ? 'btn-primary' : 'btn-ghost'}`}
            >
              All ({result.issues.length})
            </button>
            <button
              onClick={() => setSeverityFilter('security')}
              className={`btn ${severityFilter === 'security' ? 'btn-primary' : 'btn-ghost'}`}
            >
              Security ({getSeverityCount('security')})
            </button>
            <button
              onClick={() => setSeverityFilter('warning')}
              className={`btn ${severityFilter === 'warning' ? 'btn-primary' : 'btn-ghost'}`}
            >
              Warnings ({getSeverityCount('warning')})
            </button>
            <button
              onClick={() => setSeverityFilter('info')}
              className={`btn ${severityFilter === 'info' ? 'btn-primary' : 'btn-ghost'}`}
            >
              Info ({getSeverityCount('info')})
            </button>
          </div>

          {/* Issues List */}
          <div className="space-y-4">
            {filteredIssues.length === 0 ? (
              <div className="card text-center py-12">
                <svg className="mx-auto h-12 w-12 text-accent-success mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <h3 className="text-lg font-semibold text-text-primary mb-2">No Issues Found!</h3>
                <p className="text-text-secondary">Great job! Your code looks clean and well-written.</p>
              </div>
            ) : (
              filteredIssues.map((issue: Issue) => (
                <IssueCard key={issue.id} issue={issue} />
              ))
            )}
          </div>

          {/* Test Suggestions */}
          {result.tests && result.tests.length > 0 && (
            <div className="card">
              <h3 className="text-xl font-semibold text-text-primary mb-4">Test Suggestions</h3>
              <div className="space-y-3">
                {result.tests.map((test, index) => (
                  <div key={index} className="p-4 bg-tertiary-bg rounded-lg">
                    <h4 className="font-semibold text-text-primary mb-2">{test.title}</h4>
                    <p className="text-text-secondary text-sm">{test.description}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Review;
