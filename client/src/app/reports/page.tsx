import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

export default function ReportsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Reports</h1>
        <p className="text-gray-600">Generate and view detailed reports</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="border-gray-200">
          <CardHeader>
            <CardTitle className="text-gray-900">User Activity Report</CardTitle>
            <CardDescription>Detailed breakdown of user engagement and activity</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <p className="text-sm text-gray-600">Last generated: 2 days ago</p>
              <Button className="w-full">Generate Report</Button>
            </div>
          </CardContent>
        </Card>

        <Card className="border-gray-200">
          <CardHeader>
            <CardTitle className="text-gray-900">Financial Summary</CardTitle>
            <CardDescription>Monthly and quarterly financial overview</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <p className="text-sm text-gray-600">Last generated: 1 week ago</p>
              <Button className="w-full">Generate Report</Button>
            </div>
          </CardContent>
        </Card>

        <Card className="border-gray-200">
          <CardHeader>
            <CardTitle className="text-gray-900">Performance Metrics</CardTitle>
            <CardDescription>System performance and uptime statistics</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <p className="text-sm text-gray-600">Last generated: 3 days ago</p>
              <Button className="w-full">Generate Report</Button>
            </div>
          </CardContent>
        </Card>

        <Card className="border-gray-200">
          <CardHeader>
            <CardTitle className="text-gray-900">Custom Report</CardTitle>
            <CardDescription>Create your own custom report with specific metrics</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <p className="text-sm text-gray-600">Build a custom report</p>
              <Button variant="outline" className="w-full">Create Custom Report</Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
