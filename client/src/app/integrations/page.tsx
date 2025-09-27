'use client'

import { useState, useEffect, useCallback } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { useAuth } from '@/components/AuthProvider'
import { createClient } from '@/lib/supabase'
import { CheckCircle, AlertCircle, ExternalLink } from 'lucide-react'
import Image from 'next/image'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Integration {
  id: string
  integration_type: string
  external_id: string
  scopes: string[]
  metadata: Record<string, unknown>
  created_at: string
  updated_at: string
}

export default function IntegrationsPage() {
  const { user } = useAuth()
  const [integrations, setIntegrations] = useState<Integration[]>([])
  const [loading, setLoading] = useState(true)
  const [connecting, setConnecting] = useState(false)
  const [oauthProcessed, setOauthProcessed] = useState(false)
  
  // Get Shopify store from environment variable
  const shopifyStore = process.env.NEXT_PUBLIC_SHOPIFY_STORE_LINK || 'your-store.myshopify.com'

  const fetchIntegrations = useCallback(async () => {
    if (!user) {
      console.log('No user found, cannot fetch integrations')
      return
    }

    console.log('Fetching integrations for user:', user.id)

    try {
      const supabase = createClient()
      const { data, error } = await supabase
        .from('integrations')
        .select('*')
        .eq('user_id', user.id)
        .eq('is_active', true)
        .order('created_at', { ascending: false })

      if (error) {
        console.error('Error fetching integrations:', error)
        return
      }

      console.log('Fetched integrations:', data)
      setIntegrations(data || [])
    } catch (error) {
      console.error('Error fetching integrations:', error)
    } finally {
      setLoading(false)
    }
  }, [user])

  const saveIntegration = useCallback(async (tokenData: {
    access_token: string
    scopes: string[]
    shop: string
    metadata: Record<string, unknown>
  }) => {
    if (!user) {
      console.log('No user found, cannot save integration')
      return
    }

    console.log('Saving integration with data:', {
      user_id: user.id,
      integration_type: 'shopify',
      external_id: tokenData.shop,
      access_token: tokenData.access_token?.substring(0, 20) + '...',
      scopes: tokenData.scopes,
      metadata: tokenData.metadata
    })

    try {
      const supabase = createClient()
      console.log('Supabase client created, attempting upsert...')
      
      const { data, error } = await supabase
        .from('integrations')
        .upsert({
          user_id: user.id,
          integration_type: 'shopify',
          external_id: tokenData.shop,
          access_token: tokenData.access_token,
          refresh_token: null,
          token_expires_at: null,
          scopes: tokenData.scopes,
          metadata: tokenData.metadata,
          is_active: true
        }, {
          onConflict: 'user_id,integration_type,external_id'
        })
        .select()

      if (error) {
        console.error('Error saving integration:', error)
        return
      }

      console.log('Integration saved successfully:', data)
      // Refresh integrations to show the new one
      await fetchIntegrations()
    } catch (error) {
      console.error('Error saving integration:', error)
    }
  }, [user, fetchIntegrations])

  useEffect(() => {
    if (user) {
      fetchIntegrations()
    }
  }, [user, fetchIntegrations])

  // Check for OAuth success in URL params and save integration
  useEffect(() => {
    if (oauthProcessed) return // Prevent duplicate processing
    
    const urlParams = new URLSearchParams(window.location.search)
    console.log('URL params on mount:', Object.fromEntries(urlParams.entries()))
    
    if (urlParams.get('shopify_installed') === '1') {
      const shop = urlParams.get('shop')
      const tokenData = urlParams.get('token_data')
      
      console.log('OAuth success detected on mount:', { shop, tokenData: tokenData ? 'present' : 'missing', user: user ? 'present' : 'missing' })
      
      setOauthProcessed(true) // Mark as processed
      
      if (tokenData && user) {
        // Decode and save the integration
        const handleSave = async () => {
          try {
            const decodedData = JSON.parse(atob(tokenData))
            console.log('Decoded token data:', decodedData)
            await saveIntegration(decodedData)
          } catch (error) {
            console.error('Error decoding token data:', error)
          }
        }
        handleSave()
      }
      
      
      // Clean up URL after a short delay to ensure processing is complete
      setTimeout(() => {
        window.history.replaceState({}, document.title, window.location.pathname)
      }, 1000)
    }
  }, [user, saveIntegration, oauthProcessed]) // Run when user or saveIntegration changes

  const handleShopifyConnect = () => {
    setConnecting(true)
    // Open OAuth flow in new window
    const authUrl = `${API_BASE}/auth?shop=${encodeURIComponent(shopifyStore)}`
    window.open(authUrl, '_blank', 'width=600,height=700')
    
    // Clear connecting state after a delay
    setTimeout(() => {
      setConnecting(false)
    }, 10000)
  }

  const handleDisconnect = async (integrationId: string) => {
    if (!user) return

    try {
      const supabase = createClient()
      const { error } = await supabase
        .from('integrations')
        .update({ is_active: false })
        .eq('id', integrationId)
        .eq('user_id', user.id)

      if (error) {
        console.error('Error disconnecting integration:', error)
        return
      }

      await fetchIntegrations()
    } catch (error) {
      console.error('Error disconnecting integration:', error)
    }
  }


  const getIntegrationIcon = (type: string) => {
    switch (type) {
      case 'shopify':
        return (
          <Image
            src="/shopify.svg"
            alt="Shopify"
            width={20}
            height={20}
          />
        )
      default:
        return <div className="w-5 h-5 bg-gray-300 rounded" />
    }
  }

  const getIntegrationName = (type: string) => {
    switch (type) {
      case 'shopify':
        return 'Shopify'
      default:
        return type.charAt(0).toUpperCase() + type.slice(1)
    }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Integrations</h1>
          <p className="text-gray-600">Connect your favorite apps and services</p>
        </div>
        <div className="text-center text-gray-600">
          <div className="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-gray-600"></div>
          <span className="ml-2">Loading...</span>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Integrations</h1>
        <p className="text-gray-600">Connect your favorite apps and services</p>
      </div>


      {/* Available Integrations */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-3">Available Integrations</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
          {/* Shopify Integration Card */}
          <Card className="border-gray-200 hover:shadow-lg hover:border-gray-300 transition-all duration-200 group">
            <CardContent>
              <div className="flex items-center space-x-3 mb-3">
                <div className="p-1.5 bg-gray-50 rounded-md group-hover:bg-gray-100 transition-colors">
                  <Image
                    src="/shopify.svg"
                    alt="Shopify"
                    width={20}
                    height={20}
                  />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-medium text-gray-900 text-sm">Shopify</h3>
                </div>
              </div>
              <p className="text-xs text-gray-500 mb-3 line-clamp-2">
                Manage products and orders
              </p>
              <Button
                onClick={handleShopifyConnect}
                disabled={connecting}
                className="w-full bg-gray-900 hover:bg-gray-800 text-xs h-7"
                size="sm"
              >
                {connecting ? 'Connecting...' : 'Connect'}
                <ExternalLink className="w-3 h-3 ml-1.5" />
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Connected Integrations */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-3">Connected Integrations</h2>
        {integrations.length === 0 ? (
          <div className="text-center py-6 text-gray-600">
            <AlertCircle className="w-8 h-8 mx-auto mb-3 text-gray-400" />
            <p className="text-sm">No integrations connected yet</p>
            <p className="text-xs text-gray-500">Connect an app above to get started</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
            {integrations.map((integration) => (
              <Card key={integration.id} className="border-gray-200 hover:shadow-lg hover:border-gray-300 transition-all duration-200 group">
                <CardContent>
                  <div className="flex items-center space-x-3 mb-2">
                    <div className="p-1.5 bg-gray-50 rounded-md group-hover:bg-gray-100 transition-colors">
                      {getIntegrationIcon(integration.integration_type)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-1.5">
                        <h3 className="font-medium text-gray-900 text-sm truncate">
                          {getIntegrationName(integration.integration_type)}
                        </h3>
                        <Badge variant="secondary" className="bg-gray-100 text-gray-700 text-xs px-1.5 py-0.5">
                          <CheckCircle className="w-2.5 h-2.5 mr-0.5" />
                          Active
                        </Badge>
                      </div>
                      <p className="text-xs text-gray-600 truncate">
                        {integration.external_id}
                      </p>
                    </div>
                  </div>
                  
                  {integration.scopes && integration.scopes.length > 0 && (
                    <div className="flex flex-wrap gap-1 mb-2">
                      {integration.scopes.slice(0, 1).map((scope) => (
                        <Badge key={scope} variant="outline" className="text-xs px-1.5 py-0.5">
                          {scope.replace('_', ' ')}
                        </Badge>
                      ))}
                      {integration.scopes.length > 1 && (
                        <Badge variant="outline" className="text-xs px-1.5 py-0.5">
                          +{integration.scopes.length - 1}
                        </Badge>
                      )}
                    </div>
                  )}
                  
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-400">
                      {new Date(integration.created_at).toLocaleDateString()}
                    </span>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleDisconnect(integration.id)}
                      className="text-red-600 border-red-200 hover:bg-red-50 text-xs h-6 px-2"
                    >
                      Disconnect
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
