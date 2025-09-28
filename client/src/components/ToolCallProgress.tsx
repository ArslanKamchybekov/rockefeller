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
    deleteAllProducts: 'Deleting all products from your store',
    webSearch: 'Searching the web',
    marketSearch: 'Analyzing market data',
    generatePitchDeck: 'Generating pitch deck',
    generateBranding: 'Creating branding assets',
    generateBrandingVideo: 'Generating branding video'
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
    deleteAllProducts: 'Removing all products from your Shopify store',
    webSearch: 'Gathering real-time information from the web',
    marketSearch: 'Researching competitors, trends, and market statistics',
    generatePitchDeck: 'Creating comprehensive investor presentation with market research and financial models',
    generateBranding: 'Creating business name, tagline, and logo design',
    generateBrandingVideo: 'Generating promotional video content for your brand'
  }
  return descriptions[toolName] || 'Processing your request...'
}


const getProgressSteps = (toolName: string, duration: number) => {
  if (toolName === 'marketSearch') {
    const steps = [
      { name: 'Gathering market data', threshold: 5000 },
      { name: 'Analyzing competitors', threshold: 15000 },
      { name: 'Researching trends', threshold: 25000 },
      { name: 'Compiling insights', threshold: 35000 },
      { name: 'Finalizing report', threshold: 45000 }
    ]
    
    const currentStep = steps.find(step => duration < step.threshold) || steps[steps.length - 1]
    const stepIndex = steps.findIndex(step => step === currentStep)
    
    return {
      currentStep: currentStep.name,
      progress: Math.min((stepIndex + 1) / steps.length * 100, 100),
      steps
    }
  }
  
  if (toolName === 'webSearch') {
    const steps = [
      { name: 'Searching the web', threshold: 3000 },
      { name: 'Analyzing results', threshold: 8000 },
      { name: 'Compiling information', threshold: 15000 }
    ]
    
    const currentStep = steps.find(step => duration < step.threshold) || steps[steps.length - 1]
    const stepIndex = steps.findIndex(step => step === currentStep)
    
    return {
      currentStep: currentStep.name,
      progress: Math.min((stepIndex + 1) / steps.length * 100, 100),
      steps
    }
  }
  
  if (toolName === 'generatePitchDeck') {
    const steps = [
      { name: 'Researching market', threshold: 8000 },
      { name: 'Finding influencers', threshold: 16000 },
      { name: 'Generating slide content', threshold: 24000 },
      { name: 'Creating design specs', threshold: 32000 },
      { name: 'Finalizing presentation', threshold: 40000 }
    ]
    
    const currentStep = steps.find(step => duration < step.threshold) || steps[steps.length - 1]
    const stepIndex = steps.findIndex(step => step === currentStep)
    
    return {
      currentStep: currentStep.name,
      progress: Math.min((stepIndex + 1) / steps.length * 100, 100),
      steps
    }
  }
  
  return null
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

        const progressInfo = getProgressSteps(toolCall.toolName, duration)

        return (
          <div
            key={toolCall.id}
            className={cn(
              "flex items-start gap-3 p-4 rounded-lg border transition-all",
              isRunning && "bg-blue-50 border-blue-200",
              isCompleted && "bg-green-50 border-green-200",
              isError && "bg-red-50 border-red-200"
            )}
          >
            <div className="flex-shrink-0 mt-0.5">
              {isRunning && <Loader2 className="h-5 w-5 animate-spin text-blue-600" />}
              {isCompleted && <CheckCircle className="h-5 w-5 text-green-600" />}
              {isError && <XCircle className="h-5 w-5 text-red-600" />}
            </div>
            
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-2">
                <h4 className="text-sm font-medium text-gray-900 truncate">
                  {getToolDisplayName(toolCall.toolName)}
                </h4>
                <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
                  {Math.round(duration / 1000)}s
                </span>
              </div>
              
              {isRunning && progressInfo && (
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-blue-600 font-medium">
                      {progressInfo.currentStep}
                    </span>
                    <div className="flex-1 bg-gray-200 rounded-full h-1.5">
                      <div 
                        className="bg-blue-600 h-1.5 rounded-full transition-all duration-300"
                        style={{ width: `${progressInfo.progress}%` }}
                      />
                    </div>
                    <span className="text-xs text-gray-500">
                      {Math.round(progressInfo.progress)}%
                    </span>
                  </div>
                  
                  <div className="flex gap-1">
                    {progressInfo.steps.map((step, index) => (
                      <div
                        key={index}
                        className={cn(
                          "h-1 flex-1 rounded-full transition-colors",
                          duration >= step.threshold 
                            ? "bg-blue-600" 
                            : "bg-gray-200"
                        )}
                      />
                    ))}
                  </div>
                </div>
              )}
              
              <p className="text-xs text-gray-600 mt-1">
                {getToolDescription(toolCall.toolName)}
              </p>
              
              {isCompleted && toolCall.result && (
                <div className="mt-2 p-2 bg-white rounded border text-xs text-gray-700">
                  <span className="font-medium">Result:</span> {toolCall.result.message || 'Completed successfully'}
                </div>
              )}
              
              {isError && (
                <div className="mt-2 p-2 bg-red-100 rounded border border-red-200 text-xs text-red-700">
                  <span className="font-medium">Error:</span> {toolCall.result?.message || 'An error occurred'}
                </div>
              )}
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