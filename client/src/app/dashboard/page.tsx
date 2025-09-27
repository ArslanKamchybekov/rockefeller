'use client'

import { useAuth } from '@/components/AuthProvider'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export default function DashboardPage() {
  const { user } = useAuth()

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Welcome back, {user?.email}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card className="border-gray-200">
          <CardHeader>
            <CardTitle className="text-gray-900">Quick Stats</CardTitle>
            <CardDescription>Your account overview</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Account Status</span>
                <span className="text-sm font-medium text-gray-900">Active</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Email Verified</span>
                <span className="text-sm font-medium text-gray-900">
                  {user?.email_confirmed_at ? '✅ Yes' : '❌ No'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Last Login</span>
                <span className="text-sm font-medium text-gray-900">
                  {user?.last_sign_in_at ? new Date(user.last_sign_in_at).toLocaleDateString() : 'N/A'}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-gray-200">
          <CardHeader>
            <CardTitle className="text-gray-900">Recent Activity</CardTitle>
            <CardDescription>Your latest actions</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="text-sm text-gray-600">
                • Signed in successfully
              </div>
              <div className="text-sm text-gray-600">
                • Account created
              </div>
              <div className="text-sm text-gray-600">
                • Welcome email sent
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-gray-200">
          <CardHeader>
            <CardTitle className="text-gray-900">Getting Started</CardTitle>
            <CardDescription>Next steps for your account</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="text-sm text-gray-600">
                ✅ Set up authentication
              </div>
              <div className="text-sm text-gray-600">
                ✅ Access dashboard
              </div>
              <div className="text-sm text-gray-600">
                🔄 Customize your profile
              </div>
              <div className="text-sm text-gray-600">
                🔄 Connect with team
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="border-gray-200">
        <CardHeader>
          <CardTitle className="text-gray-900">Welcome to Rockefeller</CardTitle>
          <CardDescription>
            Your dashboard is ready! Here's what you can do next.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Features Available</h3>
              <ul className="space-y-1 text-sm text-gray-600">
                <li>• User authentication and management</li>
                <li>• Secure dashboard access</li>
                <li>• Responsive design with green theme</li>
                <li>• Modern UI components</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Coming Soon</h3>
              <ul className="space-y-1 text-sm text-gray-600">
                <li>• User profile management</li>
                <li>• Team collaboration tools</li>
                <li>• Advanced analytics</li>
                <li>• API integrations</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
