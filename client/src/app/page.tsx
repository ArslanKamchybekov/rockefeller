'use client'

import { useAuth } from '@/components/AuthProvider'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { ArrowRight, Zap, Target, Rocket, BarChart3, FileText, Presentation } from 'lucide-react'
import { Meteors } from '@/components/ui/meteors'
import { Ripple } from '@/components/ui/ripple'
import Link from 'next/link'

export default function Home() {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-white">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-white relative overflow-hidden">
      {/* Background Effects */}
      <Meteors 
        number={30} 
        className="opacity-10" 
        minDelay={0.5} 
        maxDelay={2} 
        minDuration={4} 
        maxDuration={10}
        angle={210}
      />
      
      {/* Ripple Effect */}
      <Ripple 
        mainCircleSize={120}
        mainCircleOpacity={0.04}
        numCircles={4}
        className="opacity-30"
      />
      
      {/* Navigation */}
      <nav className="relative z-10 bg-white/95 backdrop-blur-sm border-b border-gray-100/50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-14">
            <div className="flex items-center space-x-2">
              <h1 className="text-xl font-semibold text-gray-900">Rockefeller</h1>
            </div>
            <div className="flex items-center space-x-3">
              {user ? (
                <Link href="/dashboard">
                  <Button size="sm" className="bg-black hover:bg-gray-800 text-white h-8 px-4 text-sm font-medium">
                    Dashboard
                  </Button>
                </Link>
              ) : (
                <Link href="/login">
                  <Button size="sm" className="bg-black hover:bg-gray-800 text-white h-8 px-4 text-sm font-medium">
                    Get Started
                  </Button>
                </Link>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="relative">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <div className="inline-flex items-center px-3 py-1 rounded-full bg-gray-100 text-gray-700 text-sm font-medium mb-6">
              <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
              AI-Powered Ecommerce Platform
            </div>
            
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight tracking-tight">
              From Idea to
              <span className="text-gray-600"> Empire</span>
            </h1>
            
            <p className="text-lg text-gray-600 mb-10 max-w-3xl mx-auto leading-relaxed">
              Transform your business idea into a complete ecommerce empire. Generate stores, legal docs, marketing campaigns, and investor decks — all in minutes.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-3 justify-center items-center">
              {user ? (
                <Link href="/dashboard">
                  <Button size="sm" className="bg-black hover:bg-gray-800 text-white h-10 px-6 text-sm font-medium">
                    Launch Your Business
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
              ) : (
                <Link href="/login">
                  <Button size="sm" className="bg-black hover:bg-gray-800 text-white h-10 px-6 text-sm font-medium">
                    Start Building
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
              )}
              <Button size="sm" variant="outline" className="border-gray-200 text-gray-700 hover:bg-gray-50 h-10 px-6 text-sm font-medium">
                Watch Demo
              </Button>
            </div>
            
            {/* Stats */}
            <div className="grid grid-cols-3 gap-8 max-w-2xl mx-auto mt-16 pt-8 border-t border-gray-100">
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900 mb-1">10K+</div>
                <div className="text-sm text-gray-600">Businesses Launched</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900 mb-1">$50M+</div>
                <div className="text-sm text-gray-600">Revenue Generated</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900 mb-1">99.9%</div>
                <div className="text-sm text-gray-600">Success Rate</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16 bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-3">Everything You Need to Launch</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              From a simple business idea to a fully operational ecommerce empire
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Feature 1 */}
            <Card className="bg-white border border-gray-100 hover:border-gray-200 hover:shadow-sm transition-all duration-200 p-6">
              <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center mb-4">
                <Zap className="h-5 w-5 text-gray-700" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Instant Store Setup</h3>
              <p className="text-sm text-gray-600 leading-relaxed">
                Deploy your Shopify store with products, payment processing, and inventory management in minutes
              </p>
            </Card>

            {/* Feature 2 */}
            <Card className="bg-white border border-gray-100 hover:border-gray-200 hover:shadow-sm transition-all duration-200 p-6">
              <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center mb-4">
                <FileText className="h-5 w-5 text-gray-700" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Legal Documents</h3>
              <p className="text-sm text-gray-600 leading-relaxed">
                Generate comprehensive legal docs including privacy policies, terms of service, and NDAs
              </p>
            </Card>

            {/* Feature 3 */}
            <Card className="bg-white border border-gray-100 hover:border-gray-200 hover:shadow-sm transition-all duration-200 p-6">
              <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center mb-4">
                <Presentation className="h-5 w-5 text-gray-700" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Investor Pitch Decks</h3>
              <p className="text-sm text-gray-600 leading-relaxed">
                Create professional pitch decks with market research and influencer strategies
              </p>
            </Card>

            {/* Feature 4 */}
            <Card className="bg-white border border-gray-100 hover:border-gray-200 hover:shadow-sm transition-all duration-200 p-6">
              <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center mb-4">
                <Target className="h-5 w-5 text-gray-700" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Marketing Campaigns</h3>
              <p className="text-sm text-gray-600 leading-relaxed">
                Generate targeted ad campaigns and influencer partnerships for maximum reach
              </p>
            </Card>

            {/* Feature 5 */}
            <Card className="bg-white border border-gray-100 hover:border-gray-200 hover:shadow-sm transition-all duration-200 p-6">
              <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center mb-4">
                <BarChart3 className="h-5 w-5 text-gray-700" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Analytics & Insights</h3>
              <p className="text-sm text-gray-600 leading-relaxed">
                Track performance with detailed analytics and get actionable business insights
              </p>
            </Card>

            {/* Feature 6 */}
            <Card className="bg-white border border-gray-100 hover:border-gray-200 hover:shadow-sm transition-all duration-200 p-6">
              <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center mb-4">
                <Rocket className="h-5 w-5 text-gray-700" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Scale Automatically</h3>
              <p className="text-sm text-gray-600 leading-relaxed">
                AI-powered automation handles inventory, customer service, and growth optimization
              </p>
            </Card>
          </div>
        </div>
      </div>

      {/* How It Works Section */}
      <div className="py-16 bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-3">How It Works</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Three simple steps to launch your ecommerce empire
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-12 h-12 bg-black rounded-lg flex items-center justify-center mx-auto mb-4">
                <span className="text-lg font-bold text-white">1</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Describe Your Idea</h3>
              <p className="text-gray-600 text-sm leading-relaxed">
                Simply tell us your business idea, target market, and any specific requirements
              </p>
            </div>

            <div className="text-center">
              <div className="w-12 h-12 bg-black rounded-lg flex items-center justify-center mx-auto mb-4">
                <span className="text-lg font-bold text-white">2</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">AI Generates Everything</h3>
              <p className="text-gray-600 text-sm leading-relaxed">
                Our AI creates your store, legal docs, marketing materials, and investor presentations
              </p>
            </div>

            <div className="text-center">
              <div className="w-12 h-12 bg-black rounded-lg flex items-center justify-center mx-auto mb-4">
                <span className="text-lg font-bold text-white">3</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Launch & Scale</h3>
              <p className="text-gray-600 text-sm leading-relaxed">
                Deploy your business and watch it grow with automated optimization and scaling
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-16 bg-gray-50">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Ready to Build Your Empire?
          </h2>
          <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
            Join thousands of entrepreneurs who have already launched successful ecommerce businesses with Rockefeller
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            {user ? (
              <Link href="/dashboard">
                <Button size="sm" className="bg-black hover:bg-gray-800 text-white h-10 px-6 text-sm font-medium">
                  Launch Your Business
                  <Rocket className="ml-2 h-4 w-4" />
                </Button>
              </Link>
            ) : (
              <Link href="/login">
                <Button size="sm" className="bg-black hover:bg-gray-800 text-white h-10 px-6 text-sm font-medium">
                  Get Started Free
                  <Rocket className="ml-2 h-4 w-4" />
                </Button>
              </Link>
            )}
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-100">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <span className="text-lg font-semibold text-gray-900">Rockefeller</span>
            </div>
            <p className="text-sm text-gray-500 text-center md:text-right">
              © 2025 Rockefeller. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
