'use client'

import React from 'react'
import { cn } from '@/lib/utils'
import { CheckCircle, Loader2, Circle } from 'lucide-react'

export interface ToolCall {
  id: string
  toolName: string
  status: 'pending' | 'running' | 'completed' | 'error'
  message?: string
  result?: any
  startTime?: number
  endTime?: number
}

interface ToolCallProgressProps {
  toolCalls: ToolCall[]
  className?: string
}

const getToolDisplayName = (toolName: string) => {
  const displayNames: Record<string, string> = {
    setupStore: 'Setting up your store',
    generateDocs: 'Generating legal documents',
    configurePayment: 'Configuring payment methods',
    setupInventory: 'Setting up product inventory',
    generateLegalDocs: 'Generating comprehensive legal documents',
    // Add more tools as they're added to the system
    analyzeData: 'Analyzing your data',
    createReport: 'Creating business report',
    optimizeStore: 'Optimizing store performance',
    manageOrders: 'Managing customer orders',
    updateInventory: 'Updating product inventory',
    generateInsights: 'Generating business insights',
    setupMarketing: 'Setting up marketing campaigns',
    configureShipping: 'Configuring shipping options',
    manageCustomers: 'Managing customer data',
    processRefunds: 'Processing refunds',
    updatePricing: 'Updating product pricing',
    generateAnalytics: 'Generating analytics report',
    setupIntegrations: 'Setting up integrations',
    manageStaff: 'Managing staff accounts',
    configureTaxes: 'Configuring tax settings'
  }
  return displayNames[toolName] || toolName
}


const getToolDescription = (toolName: string) => {
  const descriptions: Record<string, string> = {
    setupStore: 'Creating store with all necessary configurations',
    generateDocs: 'Generating privacy policy and terms of service',
    configurePayment: 'Setting up payment methods',
    setupInventory: 'Creating sample products and organizing catalog',
    generateLegalDocs: 'Creating privacy policy, terms of use, and NDA documents',
    analyzeData: 'Processing data to identify trends',
    createReport: 'Compiling business reports and insights',
    optimizeStore: 'Improving performance and user experience',
    manageOrders: 'Processing and tracking orders',
    updateInventory: 'Updating stock levels',
    generateInsights: 'Analyzing data for business insights',
    setupMarketing: 'Configuring marketing campaigns',
    configureShipping: 'Setting up shipping options',
    manageCustomers: 'Organizing customer data',
    processRefunds: 'Handling refund requests',
    updatePricing: 'Adjusting product prices',
    generateAnalytics: 'Creating performance analytics',
    setupIntegrations: 'Connecting third-party services',
    manageStaff: 'Setting up team accounts',
    configureTaxes: 'Configuring tax settings'
  }
  return descriptions[toolName] || 'Processing your request...'
}

export function ToolCallProgress({ toolCalls, className }: ToolCallProgressProps) {
  if (toolCalls.length === 0) return null

  return (
    <div className={cn("space-y-3", className)}>
      <div className="text-sm font-medium text-gray-700 mb-3">Progress:</div>
      {toolCalls.map((toolCall, index) => (
        <div
          key={toolCall.id || `tool-call-${index}`}
          className={cn(
            "flex items-center gap-3 p-3 rounded-lg border transition-all duration-300",
            toolCall.status === 'completed' && "bg-green-50 border-green-200",
            toolCall.status === 'running' && "bg-blue-50 border-blue-200",
            toolCall.status === 'error' && "bg-red-50 border-red-200",
            toolCall.status === 'pending' && "bg-gray-50 border-gray-200"
          )}
        >
          {/* Status Icon */}
          <div className="flex-shrink-0">
            {toolCall.status === 'completed' ? (
              <CheckCircle className="w-5 h-5 text-green-600" />
            ) : toolCall.status === 'running' ? (
              <Loader2 className="w-5 h-5 text-blue-600 animate-spin" />
            ) : toolCall.status === 'error' ? (
              <Circle className="w-5 h-5 text-red-600 fill-current" />
            ) : (
              <Circle className="w-5 h-5 text-gray-400" />
            )}
          </div>

          {/* Tool Name and Description */}
          <div className="flex-1 min-w-0">
            <div className={cn(
              "text-sm font-medium",
              toolCall.status === 'completed' && "text-gray-800",
              toolCall.status === 'running' && "text-gray-800",
              toolCall.status === 'error' && "text-gray-800",
              toolCall.status === 'pending' && "text-gray-600"
            )}>
              {getToolDisplayName(toolCall.toolName)}
            </div>
            {toolCall.status === 'running' && (
              <div className="text-xs text-gray-500 mt-1">
                {getToolDescription(toolCall.toolName)}
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  )
}

// Individual tool call item component
export function ToolCallItem({ 
  toolCall, 
  className 
}: { 
  toolCall: ToolCall
  className?: string 
}) {
  return (
    <div
      className={cn(
        "flex items-center gap-3 p-2 rounded-lg border transition-all duration-300",
        toolCall.status === 'completed' && "bg-green-50 border-green-200",
        toolCall.status === 'running' && "bg-blue-50 border-blue-200",
        toolCall.status === 'error' && "bg-red-50 border-red-200",
        toolCall.status === 'pending' && "bg-gray-50 border-gray-200",
        className
      )}
    >
      {/* Status Icon */}
      <div className="flex-shrink-0">
        {toolCall.status === 'completed' ? (
          <CheckCircle className="w-4 h-4 text-green-600" />
        ) : toolCall.status === 'running' ? (
          <Loader2 className="w-4 h-4 text-blue-600 animate-spin" />
        ) : toolCall.status === 'error' ? (
          <Circle className="w-4 h-4 text-red-600 fill-current" />
        ) : (
          <Circle className="w-4 h-4 text-gray-400" />
        )}
      </div>

      {/* Tool Info */}
      <div className="flex-1 min-w-0">
        <div className={cn(
          "text-sm font-medium truncate",
          toolCall.status === 'completed' && "text-gray-800",
          toolCall.status === 'running' && "text-gray-800",
          toolCall.status === 'error' && "text-gray-800",
          toolCall.status === 'pending' && "text-gray-600"
        )}>
          {getToolDisplayName(toolCall.toolName)}
        </div>
        {toolCall.status === 'running' && (
          <div className="text-xs text-gray-500 truncate">
            {getToolDescription(toolCall.toolName)}
          </div>
        )}
      </div>

      {/* Status Badge */}
      <div className={cn(
        "text-xs px-2 py-1 rounded-full",
        toolCall.status === 'completed' && "bg-green-100 text-green-700",
        toolCall.status === 'running' && "bg-blue-100 text-blue-700",
        toolCall.status === 'error' && "bg-red-100 text-red-700",
        toolCall.status === 'pending' && "bg-gray-100 text-gray-600"
      )}>
        {toolCall.status === 'completed' ? 'Completed' :
         toolCall.status === 'running' ? 'In progress' :
         toolCall.status === 'error' ? 'Failed' :
         'Waiting'}
      </div>
    </div>
  )
}
