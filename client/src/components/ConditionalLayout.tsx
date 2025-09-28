'use client'

import { usePathname } from 'next/navigation'
import { useAuth } from '@/components/AuthProvider'
import { AppSidebar } from '@/components/AppSidebar'
import { SidebarProvider, SidebarInset } from '@/components/ui/sidebar'

interface ConditionalLayoutProps {
  children: React.ReactNode
}

export default function ConditionalLayout({ children }: ConditionalLayoutProps) {
  const pathname = usePathname()
  const { user } = useAuth()

  // Pages that should not have the sidebar
  const noSidebarPages = ['/login', '/auth/callback', '/']
  
  // Pages that need full height without padding (like chat)
  const fullHeightPages = ['/chat']
  
  // If user is not authenticated and not on a public page, redirect to login
  if (!user && !noSidebarPages.includes(pathname)) {
    // This will be handled by middleware, but we can show loading here
    return (
      <main className="flex-1 overflow-auto bg-gray-50 min-h-screen">
          {children}
      </main>
    )
  }

  // If on a page that shouldn't have sidebar, render without sidebar
  if (noSidebarPages.includes(pathname)) {
    return (
      <main className="flex-1 overflow-auto bg-gray-50 min-h-screen">
          {children}
      </main>
    )
  }

  // For full height pages (like chat), render without padding and overflow
  if (fullHeightPages.includes(pathname)) {
    return (
      <SidebarProvider>
        <AppSidebar />
        <SidebarInset>
          <main className="flex-1 bg-gray-50 h-screen overflow-hidden">
            {children}
          </main>
        </SidebarInset>
      </SidebarProvider>
    )
  }

  // For all other pages, render with sidebar
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <main className="flex-1 overflow-auto bg-gray-50 min-h-screen">
          <div className="p-6">
            {children}
          </div>
        </main>
      </SidebarInset>
    </SidebarProvider>
  )
}
