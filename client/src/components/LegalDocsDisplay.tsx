'use client'

import React from 'react'
import { cn } from '@/lib/utils'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

interface LegalDocument {
  type: string
  title: string
  summary: string
  content: string
  placeholders: string[]
  defaults_used: Record<string, any>
}

interface PDFInfo {
  title: string
  filename: string
  pdf_data: string
  size: number
  error?: string
}

interface LegalDocsDisplayProps {
  docs: LegalDocument[]
  pdfs?: PDFInfo[]
  className?: string
}

export function LegalDocsDisplay({ docs, pdfs = [], className }: LegalDocsDisplayProps) {
  const [expandedKeys, setExpandedKeys] = React.useState<Set<string>>(new Set())

  const filenameFromTitle = (title: string) => `${title.replace(/\s+/g, '_').toLowerCase()}.md`

  const downloadPDF = (pdf: PDFInfo) => {
    if (!pdf.pdf_data) {
      console.error('No PDF data available for', pdf.title);
      return;
    }

    try {
      // Convert base64 to blob
      const byteCharacters = atob(pdf.pdf_data);
      const byteNumbers = new Array(byteCharacters.length);
      for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
      }
      const byteArray = new Uint8Array(byteNumbers);
      const blob = new Blob([byteArray], { type: 'application/pdf' });

      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = pdf.filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error downloading PDF:', error);
    }
  }

  const getPDFForDoc = (docTitle: string) => {
    return pdfs.find(pdf => pdf.title === docTitle);
  }

  const getDocIcon = (type: string) => {
    switch (type) {
      case 'privacy_policy_bootstrap':
        return '🔒'
      case 'website_terms_bootstrap':
        return '📋'
      case 'nda_mutual_short':
        return '🤝'
      default:
        return '📄'
    }
  }

  if (!docs || docs.length === 0) {
    return null
  }

  return (
    <div className={cn("space-y-3", className)}>
      {docs.map((doc, index) => {
        const key = `${doc.type}-${index}`
        const isExpanded = expandedKeys.has(key)
        const filename = filenameFromTitle(doc.title)
        const pdf = getPDFForDoc(doc.title)
        return (
          <div key={key} className="border rounded-md">
            <div className="flex items-center justify-between p-2">
              <button
                type="button"
                className="flex-1 flex items-center gap-2 text-left hover:bg-gray-50 rounded p-1"
                onClick={() => {
                  setExpandedKeys((prev) => {
                    const next = new Set(prev)
                    if (next.has(key)) next.delete(key); else next.add(key)
                    return next
                  })
                }}
              >
                <span className="text-base">{getDocIcon(doc.type)}</span>
                <span className="text-sm text-gray-900 font-medium">{filename}</span>
              </button>
              
              <div className="flex items-center gap-2">
                {pdf && pdf.pdf_data && (
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      downloadPDF(pdf);
                    }}
                    className="flex items-center gap-1 px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded hover:bg-blue-200 transition-colors"
                    title={`Download PDF (${Math.round(pdf.size / 1024)}KB)`}
                  >
                    📄 PDF
                  </button>
                )}
                
                <button
                  type="button"
                  onClick={() => {
                    setExpandedKeys((prev) => {
                      const next = new Set(prev)
                      if (next.has(key)) next.delete(key); else next.add(key)
                      return next
                    })
                  }}
                >
                  <svg
                    className={cn(
                      "w-4 h-4 text-gray-600 transition-transform",
                      isExpanded ? "rotate-180" : "rotate-0"
                    )}
                    viewBox="0 0 20 20"
                    fill="currentColor"
                    aria-hidden="true"
                  >
                    <path fillRule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 10.94l3.71-3.71a.75.75 0 111.06 1.06l-4.24 4.24a.75.75 0 01-1.06 0L5.21 8.29a.75.75 0 01.02-1.08z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>

            {isExpanded && (
              <div className="bg-white border-t p-4">
                <div className="prose max-w-none">
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                  >
                    {doc.content}
                  </ReactMarkdown>
                </div>
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}
