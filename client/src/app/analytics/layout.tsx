'use client'

import { AppSidebar } from '@/components/AppSidebar'
import { SidebarProvider, SidebarInset } from '@/components/ui/sidebar'

export default function AnalyticsLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <main className="flex-1 overflow-auto bg-green-50 min-h-screen">
          <div className="p-6">
            {children}
          </div>
        </main>
      </SidebarInset>
    </SidebarProvider>
  )
}
