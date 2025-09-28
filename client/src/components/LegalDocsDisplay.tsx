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

interface LegalDocsDisplayProps {
  docs: LegalDocument[]
  className?: string
}

export function LegalDocsDisplay({ docs, className }: LegalDocsDisplayProps) {
  const [expandedKeys, setExpandedKeys] = React.useState<Set<string>>(new Set())

  const filenameFromTitle = (title: string) => `${title.replace(/\s+/g, '_').toLowerCase()}.md`

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
        return (
          <div key={key} className="border rounded-md">
            <button
              type="button"
              className="w-full flex items-center justify-between p-2 hover:bg-gray-50"
              onClick={() => {
                setExpandedKeys((prev) => {
                  const next = new Set(prev)
                  if (next.has(key)) next.delete(key); else next.add(key)
                  return next
                })
              }}
            >
              <div className="flex items-center gap-2 text-left">
                <span className="text-base">{getDocIcon(doc.type)}</span>
                <span className="text-sm text-gray-900 font-medium">{filename}</span>
              </div>
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
