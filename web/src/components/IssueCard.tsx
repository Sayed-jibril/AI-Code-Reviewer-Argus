import React from 'react';
import { Issue } from '../api';

interface IssueCardProps {
  issue: Issue;
}

const IssueCard: React.FC<IssueCardProps> = ({ issue }) => {
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'security':
        return 'text-accent-error border-accent-error bg-red-900/20';
      case 'warning':
        return 'text-accent-warning border-accent-warning bg-yellow-900/20';
      case 'error':
        return 'text-accent-error border-accent-error bg-red-900/20';
      case 'info':
        return 'text-accent-info border-accent-info bg-blue-900/20';
      default:
        return 'text-text-secondary border-border-color bg-card-bg';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'security':
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
        );
      case 'warning':
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
        );
      case 'error':
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
      case 'info':
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
      default:
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
    }
  };

  return (
    <div className={`card border-l-4 ${getSeverityColor(issue.severity)}`}>
      <div className="flex items-start space-x-4">
        <div className="flex-shrink-0 mt-1">
          {getSeverityIcon(issue.severity)}
        </div>
        
        <div className="flex-1 min-w-0">
          {/* Header */}
          <div className="flex items-start justify-between mb-3">
            <div>
              <h3 className="text-lg font-semibold text-text-primary mb-1">
                {issue.title}
              </h3>
              <div className="flex items-center space-x-4 text-sm text-text-muted">
                <span className="font-mono">{issue.filePath}</span>
                <span>Line {issue.lineStart}{issue.lineEnd !== issue.lineStart ? `-${issue.lineEnd}` : ''}</span>
                <span className="capitalize">{issue.severity}</span>
                <span>Confidence: {Math.round(issue.confidence * 100)}%</span>
              </div>
            </div>
            
            <div className="flex space-x-2">
              {issue.tags.map((tag, index) => (
                <span
                  key={index}
                  className="px-2 py-1 text-xs font-medium bg-tertiary-bg text-text-secondary rounded-md"
                >
                  {tag}
                </span>
              ))}
            </div>
          </div>

          {/* Content */}
          <div className="space-y-3">
            {issue.explanation && (
              <div>
                <h4 className="text-sm font-semibold text-text-primary mb-1">Explanation</h4>
                <p className="text-sm text-text-secondary">{issue.explanation}</p>
              </div>
            )}

            {issue.suggestion && (
              <div>
                <h4 className="text-sm font-semibold text-text-primary mb-1">Suggestion</h4>
                <p className="text-sm text-text-secondary">{issue.suggestion}</p>
              </div>
            )}

            {issue.codeFrame && (
              <div>
                <h4 className="text-sm font-semibold text-text-primary mb-2">Code Context</h4>
                <pre className="text-sm bg-tertiary-bg p-3 rounded-lg overflow-x-auto text-text-secondary font-mono">
                  {issue.codeFrame}
                </pre>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="mt-4 pt-3 border-t border-border-color">
            <div className="flex items-center justify-between text-xs text-text-muted">
              <span>Rule ID: {issue.ruleId}</span>
              <span>Issue ID: {issue.id}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default IssueCard;
