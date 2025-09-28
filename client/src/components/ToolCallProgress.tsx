'use client'

import { cn } from '@/lib/utils'
import { CheckCircle, Clock, Loader2, XCircle } from 'lucide-react'

export interface ToolCall {
  id: string
  toolName: string
  status: 'running' | 'completed' | 'error'
  startTime: number
  endTime?: number
  result?: any
}     

interface ToolCallProgressProps {
  toolCalls: ToolCall[]
  className?: string
}

const getToolDisplayName = (toolName: string) => {
  const displayNames: Record<string, string> = {
    setupStore: 'Setting up your store',
    configurePayment: 'Configuring payment methods',
    setupInventory: 'Setting up product inventory',
    generateLegalDocs: 'Generating comprehensive legal documents',
    addProduct: 'Adding product to your store',
    deleteProduct: 'Deleting product from your store',
    deleteAllProducts: 'Deleting all products from your store'
  }
  return displayNames[toolName] || toolName
}

const getToolDescription = (toolName: string) => {
  const descriptions: Record<string, string> = {
    setupStore: 'Creating store with all necessary configurations',
    configurePayment: 'Setting up payment methods',
    setupInventory: 'Creating sample products and organizing catalog',
    generateLegalDocs: 'Creating privacy policy, terms of use, and NDA documents',
    addProduct: 'Adding new product to your Shopify store',
    deleteProduct: 'Removing product from your Shopify store',
    deleteAllProducts: 'Removing all products from your Shopify store'
  }
  return descriptions[toolName] || 'Processing your request...'
}

export function ToolCallProgress({ toolCalls, className }: ToolCallProgressProps) {
  if (toolCalls.length === 0) return null

  return (
    <div className={cn("space-y-3", className)}>
      {toolCalls.map((toolCall) => {
        const isRunning = toolCall.status === 'running'
        const isCompleted = toolCall.status === 'completed'
        const isError = toolCall.status === 'error'
        
        const duration = toolCall.endTime 
          ? toolCall.endTime - toolCall.startTime
          : Date.now() - toolCall.startTime

        return (
          <div
            key={toolCall.id}
            className={cn(
              "flex items-center gap-3 p-3 rounded-lg border transition-all",
              isRunning && "bg-blue-50 border-blue-200",
              isCompleted && "bg-green-50 border-green-200",
              isError && "bg-red-50 border-red-200"
            )}
          >
            <div className="flex-shrink-0">
              {isRunning && <Loader2 className="h-5 w-5 animate-spin text-blue-600" />}
              {isCompleted && <CheckCircle className="h-5 w-5 text-green-600" />}
              {isError && <XCircle className="h-5 w-5 text-red-600" />}
            </div>
            
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <h4 className="text-sm font-medium text-gray-900 truncate">
                  {getToolDisplayName(toolCall.toolName)}
                </h4>
                <span className="text-xs text-gray-500">
                  {Math.round(duration / 1000)}s
                </span>
              </div>
              <p className="text-xs text-gray-600 mt-1">
                {getToolDescription(toolCall.toolName)}
              </p>
            </div>
            
            <div className="flex-shrink-0">
              <Clock className="h-4 w-4 text-gray-400" />
            </div>
          </div>
        )
      })}
    </div>
  )
}