'use client'

import React from 'react'
import { cn } from '@/lib/utils'
import { X, Download, Copy, Check, FileText } from 'lucide-react'
import { Button } from '@/components/ui/button'
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

interface DocumentViewerProps {
  document: LegalDocument
  isOpen: boolean
  onClose: () => void
}

export function DocumentViewer({ document: doc, isOpen, onClose }: DocumentViewerProps) {
  const [copied, setCopied] = React.useState(false)

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(doc.content)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy text: ', err)
    }
  }

  const downloadDoc = () => {
    const blob = new Blob([doc.content], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = window.document.createElement('a')
    a.href = url
    a.download = `${doc.title.replace(/\s+/g, '_').toLowerCase()}.md`
    window.document.body.appendChild(a)
    a.click()
    window.document.body.removeChild(a)
    URL.revokeObjectURL(url)
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

  const getDocColor = (type: string) => {
    switch (type) {
      case 'privacy_policy_bootstrap':
        return 'border-blue-200 bg-blue-50'
      case 'website_terms_bootstrap':
        return 'border-green-200 bg-green-50'
      case 'nda_mutual_short':
        return 'border-purple-200 bg-purple-50'
      default:
        return 'border-gray-200 bg-gray-50'
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />
      
      {/* Modal */}
      <div className="relative bg-white rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className={cn(
          "flex items-center justify-between p-6 border-b rounded-t-lg",
          getDocColor(doc.type)
        )}>
          <div className="flex items-center gap-3">
            <span className="text-3xl">{getDocIcon(doc.type)}</span>
            <div>
              <h2 className="text-xl font-semibold text-gray-900">
                {doc.title}
              </h2>
              <p className="text-sm text-gray-600 mt-1">
                {doc.summary}
              </p>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={copyToClipboard}
              className="flex items-center gap-2"
            >
              {copied ? (
                <Check className="w-4 h-4 text-green-600" />
              ) : (
                <Copy className="w-4 h-4" />
              )}
              {copied ? 'Copied!' : 'Copy'}
            </Button>
            
            <Button
              variant="outline"
              size="sm"
              onClick={downloadDoc}
              className="flex items-center gap-2"
            >
              <Download className="w-4 h-4" />
              Download
            </Button>
            
            <Button
              variant="ghost"
              size="sm"
              onClick={onClose}
              className="p-2"
            >
              <X className="w-4 h-4" />
            </Button>
          </div>
        </div>

        {/* Placeholders Info */}
        {doc.placeholders && doc.placeholders.length > 0 && (
          <div className="p-4 bg-yellow-50 border-b border-yellow-200">
            <h3 className="text-sm font-medium text-yellow-800 mb-2">
              📝 Placeholders to Replace:
            </h3>
            <div className="flex flex-wrap gap-2">
              {doc.placeholders.map((placeholder, idx) => (
                <span
                  key={idx}
                  className="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded-full"
                >
                  {placeholder}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          <div className="prose prose-lg max-w-none">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                h1: ({ children }) => (
                  <h1 className="text-2xl font-bold mt-8 mb-4 first:mt-0 text-gray-900 border-b border-gray-200 pb-2">
                    {children}
                  </h1>
                ),
                h2: ({ children }) => (
                  <h2 className="text-xl font-semibold mt-6 mb-3 first:mt-0 text-gray-900">
                    {children}
                  </h2>
                ),
                h3: ({ children }) => (
                  <h3 className="text-lg font-semibold mt-4 mb-2 first:mt-0 text-gray-800">
                    {children}
                  </h3>
                ),
                h4: ({ children }) => (
                  <h4 className="text-base font-semibold mt-3 mb-2 first:mt-0 text-gray-800">
                    {children}
                  </h4>
                ),
                p: ({ children }) => (
                  <p className="my-4 first:mt-0 last:mb-0 leading-relaxed text-gray-700">
                    {children}
                  </p>
                ),
                ul: ({ children }) => (
                  <ul className="my-4 space-y-2 list-disc pl-6">{children}</ul>
                ),
                ol: ({ children }) => (
                  <ol className="my-4 space-y-2 list-decimal pl-6">{children}</ol>
                ),
                li: ({ children }) => (
                  <li className="leading-relaxed text-gray-700">{children}</li>
                ),
                strong: ({ children }) => (
                  <strong className="font-semibold text-gray-900">{children}</strong>
                ),
                em: ({ children }) => (
                  <em className="italic text-gray-700">{children}</em>
                ),
                blockquote: ({ children }) => (
                  <blockquote className="border-l-4 border-gray-300 pl-4 my-4 italic text-gray-600 bg-gray-50 py-2">
                    {children}
                  </blockquote>
                ),
                code: ({ children, className }) => {
                  const isInline = !className
                  return isInline ? (
                    <code className="bg-gray-100 text-gray-800 px-1.5 py-0.5 rounded text-sm font-mono">
                      {children}
                    </code>
                  ) : (
                    <code className={className}>{children}</code>
                  )
                },
                pre: ({ children }) => (
                  <pre className="bg-gray-100 border border-gray-200 p-4 rounded-lg overflow-x-auto my-4">
                    {children}
                  </pre>
                ),
              }}
            >
              {doc.content}
            </ReactMarkdown>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 bg-gray-50 border-t border-gray-200 rounded-b-lg">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <div className="flex items-center gap-2">
              <FileText className="w-4 h-4" />
              <span>Legal Document Template</span>
            </div>
            <p>
              ⚖️ Review with a legal professional before use
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
