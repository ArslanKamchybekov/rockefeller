import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
        <p className="text-gray-600">View your performance metrics and insights</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="border-gray-200">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Total Users</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">1,234</div>
            <p className="text-xs text-gray-600">+20.1% from last month</p>
          </CardContent>
        </Card>

        <Card className="border-gray-200">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Active Sessions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">567</div>
            <p className="text-xs text-gray-600">+12.5% from last week</p>
          </CardContent>
        </Card>

        <Card className="border-gray-200">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Conversion Rate</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">3.2%</div>
            <p className="text-xs text-gray-600">+0.5% from last month</p>
          </CardContent>
        </Card>

        <Card className="border-gray-200">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Revenue</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">$45,231</div>
            <p className="text-xs text-gray-600">+15.3% from last month</p>
          </CardContent>
        </Card>
      </div>

      <Card className="border-gray-200">
        <CardHeader>
          <CardTitle className="text-gray-900">Analytics Overview</CardTitle>
          <CardDescription>Coming soon - detailed analytics and reporting features</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center h-64 bg-gray-50 rounded-lg border-2 border-dashed border-gray-200">
            <p className="text-gray-600">Analytics charts and graphs will appear here</p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
