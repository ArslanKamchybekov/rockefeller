'use client'

import { useAuth } from '@/components/AuthProvider'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export default function Home() {
  const { user, loading, signOut } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-xl text-gray-900">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">Rockefeller App</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">Welcome, {user?.email}</span>
              <Button
                onClick={signOut}
                variant="outline"
                className="border-red-200 text-red-600 hover:bg-red-50 hover:border-red-300"
              >
                Sign Out
              </Button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <Card className="border-gray-200">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl text-gray-900">
                🎉 Welcome to Rockefeller App!
              </CardTitle>
              <CardDescription className="text-gray-600">
                You have successfully authenticated with Supabase
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                <h3 className="font-medium text-gray-900 mb-2">User Information</h3>
                <div className="space-y-1 text-sm text-gray-700">
                  <div><strong>User ID:</strong> {user?.id}</div>
                  <div><strong>Email:</strong> {user?.email}</div>
                  <div><strong>Email Confirmed:</strong> {user?.email_confirmed_at ? 'Yes' : 'No'}</div>
                  <div><strong>Last Sign In:</strong> {user?.last_sign_in_at ? new Date(user.last_sign_in_at).toLocaleDateString() : 'N/A'}</div>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card className="border-gray-100">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-lg text-gray-900">Getting Started</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-600 mb-3">
                      Your authentication is now set up and working perfectly!
                    </p>
                    <ul className="text-sm text-gray-700 space-y-1">
                      <li>✅ Supabase authentication</li>
                      <li>✅ Protected routes</li>
                      <li>✅ Session management</li>
                      <li>✅ Clean green UI</li>
                    </ul>
                  </CardContent>
                </Card>
                
                <Card className="border-gray-100">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-lg text-gray-900">Next Steps</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-600 mb-3">
                      Ready to build your application features:
                    </p>
                    <ul className="text-sm text-gray-700 space-y-1">
                      <li>• Add user profiles</li>
                      <li>• Create dashboard features</li>
                      <li>• Integrate with FastAPI backend</li>
                      <li>• Build your core functionality</li>
                    </ul>
                  </CardContent>
                </Card>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
