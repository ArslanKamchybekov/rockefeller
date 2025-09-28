'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Download, Eye, Share2, Edit3 } from 'lucide-react'
import { cn } from '@/lib/utils'

interface Slide {
  id: number
  title: string
  content: string[]
  visual_suggestions?: string[]
  icon?: string
}

interface PitchDeckData {
  deck_id: string
  idea: string
  market_research: string
  financial_model: string
  deck_content: string
  design_specs: string
}

export default function PitchDeckPage({ params }: { params: { id: string } }) {
  const [deckData, setDeckData] = useState<PitchDeckData | null>(null)
  const [slides, setSlides] = useState<Slide[]>([])
  const [currentSlide, setCurrentSlide] = useState(0)
  const [isLoading, setIsLoading] = useState(true)
  const [isExporting, setIsExporting] = useState(false)

  useEffect(() => {
    // In a real app, you'd fetch this from an API or database
    // For now, we'll simulate the data
    const mockDeckData: PitchDeckData = {
      deck_id: params.id,
      idea: "AI-powered Shopify store management platform",
      market_research: "Market research data...",
      financial_model: "Financial model data...",
      deck_content: JSON.stringify({
        slides: [
          {
            id: 1,
            title: "AI Store Manager",
            content: [
              "Revolutionary AI platform for Shopify store management",
              "Automated inventory, marketing, and customer service",
              "Founded 2024 • San Francisco, CA"
            ],
            icon: "🤖"
          },
          {
            id: 2,
            title: "The Problem",
            content: [
              "Shopify store owners spend 20+ hours/week on manual tasks",
              "Inventory management is error-prone and time-consuming",
              "Customer service response times are inconsistent",
              "Marketing campaigns lack personalization"
            ],
            icon: "😤"
          },
          {
            id: 3,
            title: "Our Solution",
            content: [
              "AI-powered automation for all store operations",
              "Intelligent inventory forecasting and management",
              "24/7 AI customer service with human-like responses",
              "Personalized marketing campaigns that convert"
            ],
            icon: "✨"
          },
          {
            id: 4,
            title: "Market Opportunity",
            content: [
              "TAM: $15.2B (Global E-commerce Software Market)",
              "SAM: $2.1B (Shopify Ecosystem)",
              "SOM: $150M (AI-powered store management)",
              "Growing 25% YoY with increasing AI adoption"
            ],
            icon: "📈"
          },
          {
            id: 5,
            title: "Business Model",
            content: [
              "SaaS subscription: $99-499/month per store",
              "Enterprise plans: $1,000+/month",
              "Transaction fees: 0.5% on processed orders",
              "Professional services: $200/hour"
            ],
            icon: "💰"
          },
          {
            id: 6,
            title: "Traction",
            content: [
              "50+ beta customers with 95% satisfaction",
              "$25K MRR in first 6 months",
              "Featured in Shopify App Store top 10",
              "Partnerships with 3 major agencies"
            ],
            icon: "🚀"
          },
          {
            id: 7,
            title: "Competition",
            content: [
              "Shopify Apps: Basic automation, limited AI",
              "Enterprise Solutions: Expensive, complex setup",
              "Our Advantage: True AI, easy setup, affordable",
              "Unique: End-to-end store management platform"
            ],
            icon: "⚔️"
          },
          {
            id: 8,
            title: "Team",
            content: [
              "CEO: Former Shopify Product Manager (5 years)",
              "CTO: Ex-Google AI Engineer (8 years)",
              "Head of Sales: Former HubSpot VP (6 years)",
              "Advisors: 2 successful e-commerce exits"
            ],
            icon: "👥"
          },
          {
            id: 9,
            title: "Financial Projections",
            content: [
              "Year 1: $500K ARR, 200 customers",
              "Year 2: $2.5M ARR, 800 customers",
              "Year 3: $8M ARR, 2,000 customers",
              "Gross margin: 85% • Break-even: Month 18"
            ],
            icon: "📊"
          },
          {
            id: 10,
            title: "The Ask",
            content: [
              "Seeking $2M Series A funding",
              "Use of funds: 60% engineering, 30% sales, 10% ops",
              "18-month runway to $5M ARR",
              "Next milestone: 1,000 paying customers"
            ],
            icon: "🎯"
          }
        ]
      }),
      design_specs: JSON.stringify({
        primary_color: "#3B82F6",
        secondary_color: "#1E40AF",
        accent_color: "#F59E0B",
        font_heading: "Inter Bold",
        font_body: "Inter Regular"
      })
    }

    setTimeout(() => {
      setDeckData(mockDeckData)
      try {
        const parsedContent = JSON.parse(mockDeckData.deck_content)
        setSlides(parsedContent.slides || [])
      } catch (error) {
        console.error('Error parsing deck content:', error)
      }
      setIsLoading(false)
    }, 1000)
  }, [params.id])

  const handleExportPDF = async () => {
    setIsExporting(true)
    try {
      const response = await fetch('/api/pitchdeck/export', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          deckId: params.id,
          slides: slides
        })
      })

      if (!response.ok) {
        throw new Error('Export failed')
      }

      // Create blob and download
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `pitch-deck-${params.id}.pdf`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Export failed:', error)
      alert('Failed to export PDF. Please try again.')
    } finally {
      setIsExporting(false)
    }
  }

  const nextSlide = () => {
    setCurrentSlide((prev) => Math.min(prev + 1, slides.length - 1))
  }

  const prevSlide = () => {
    setCurrentSlide((prev) => Math.max(prev - 1, 0))
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading pitch deck...</p>
        </div>
      </div>
    )
  }

  if (!deckData || slides.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">Pitch deck not found</p>
        </div>
      </div>
    )
  }

  const currentSlideData = slides[currentSlide]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold text-gray-900">{deckData.idea}</h1>
            <p className="text-sm text-gray-600">Pitch Deck Preview</p>
          </div>
          <div className="flex items-center gap-3">
            <Button variant="outline" size="sm">
              <Edit3 className="h-4 w-4 mr-2" />
              Edit
            </Button>
            <Button variant="outline" size="sm">
              <Share2 className="h-4 w-4 mr-2" />
              Share
            </Button>
            <Button 
              onClick={handleExportPDF} 
              disabled={isExporting}
              size="sm"
            >
              <Download className="h-4 w-4 mr-2" />
              {isExporting ? 'Exporting...' : 'Export PDF'}
            </Button>
          </div>
        </div>
      </div>

      <div className="flex">
        {/* Slide Navigation */}
        <div className="w-64 bg-white border-r border-gray-200 p-4">
          <h3 className="font-medium text-gray-900 mb-4">Slides</h3>
          <div className="space-y-2">
            {slides.map((slide, index) => (
              <button
                key={slide.id}
                onClick={() => setCurrentSlide(index)}
                className={cn(
                  "w-full text-left p-3 rounded-lg border transition-colors",
                  currentSlide === index
                    ? "bg-blue-50 border-blue-200 text-blue-900"
                    : "bg-gray-50 border-gray-200 text-gray-700 hover:bg-gray-100"
                )}
              >
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-lg">{slide.icon}</span>
                  <span className="text-sm font-medium">Slide {slide.id}</span>
                </div>
                <p className="text-xs text-gray-600 truncate">{slide.title}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Main Slide Display */}
        <div className="flex-1 p-8">
          <div className="max-w-4xl mx-auto">
            <Card className="aspect-[16/9] bg-white shadow-lg">
              <div className="h-full p-12 flex flex-col justify-center">
                <div className="text-center mb-8">
                  <div className="text-6xl mb-4">{currentSlideData.icon}</div>
                  <h2 className="text-4xl font-bold text-gray-900 mb-4">
                    {currentSlideData.title}
                  </h2>
                </div>
                
                <div className="space-y-4">
                  {currentSlideData.content.map((point, index) => (
                    <div key={index} className="flex items-start gap-3">
                      <div className="w-2 h-2 bg-blue-600 rounded-full mt-3 flex-shrink-0"></div>
                      <p className="text-lg text-gray-700">{point}</p>
                    </div>
                  ))}
                </div>
              </div>
            </Card>

            {/* Navigation Controls */}
            <div className="flex items-center justify-between mt-6">
              <Button
                onClick={prevSlide}
                disabled={currentSlide === 0}
                variant="outline"
              >
                Previous
              </Button>
              
              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-600">
                  {currentSlide + 1} of {slides.length}
                </span>
                <div className="flex gap-1">
                  {slides.map((_, index) => (
                    <div
                      key={index}
                      className={cn(
                        "w-2 h-2 rounded-full",
                        currentSlide === index ? "bg-blue-600" : "bg-gray-300"
                      )}
                    />
                  ))}
                </div>
              </div>

              <Button
                onClick={nextSlide}
                disabled={currentSlide === slides.length - 1}
                variant="outline"
              >
                Next
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
