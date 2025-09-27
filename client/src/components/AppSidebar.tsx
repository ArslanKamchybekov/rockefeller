'use client'

import { useAuth } from '@/components/AuthProvider'
import { Button } from '@/components/ui/button'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from '@/components/ui/sidebar'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { 
  Home, 
  User, 
  Settings, 
  BarChart3, 
  FileText, 
  HelpCircle,
  LogOut,
  ChevronUp
} from 'lucide-react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

const navigation = [
  {
    title: 'Main',
    items: [
      { title: 'Dashboard', url: '/dashboard', icon: Home },
      { title: 'Analytics', url: '/analytics', icon: BarChart3 },
      { title: 'Reports', url: '/reports', icon: FileText },
    ],
  },
  {
    title: 'Account',
    items: [
      { title: 'Profile', url: '/profile', icon: User },
      { title: 'Settings', url: '/settings', icon: Settings },
      { title: 'Help', url: '/help', icon: HelpCircle },
    ],
  },
]

export function AppSidebar() {
  const { user, signOut } = useAuth()
  const pathname = usePathname()

  const getUserInitials = (email?: string) => {
    if (!email) return 'U'
    return email.charAt(0).toUpperCase()
  }

  return (
    <Sidebar className="border-green-200">
      <SidebarHeader className="border-b border-green-100">
        <div className="flex items-center gap-2 px-4 py-2">
          <div className="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">R</span>
          </div>
          <span className="font-semibold text-green-800">Rockefeller</span>
        </div>
      </SidebarHeader>
      
      <SidebarContent>
        {navigation.map((group) => (
          <SidebarGroup key={group.title}>
            <SidebarGroupLabel className="text-green-700">{group.title}</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {group.items.map((item) => (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton
                      asChild
                      isActive={pathname === item.url}
                      className="data-[active=true]:bg-green-100 data-[active=true]:text-green-800 hover:bg-green-50 hover:text-green-700"
                    >
                      <Link href={item.url}>
                        <item.icon className="w-4 h-4" />
                        <span>{item.title}</span>
                      </Link>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        ))}
      </SidebarContent>
      
      <SidebarFooter className="border-t border-green-100">
        <SidebarMenu>
          <SidebarMenuItem>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <SidebarMenuButton className="hover:bg-green-50">
                  <Avatar className="w-6 h-6">
                    <AvatarFallback className="bg-green-100 text-green-700 text-xs">
                      {getUserInitials(user?.email)}
                    </AvatarFallback>
                  </Avatar>
                  <div className="flex flex-col items-start text-left">
                    <span className="text-sm font-medium text-green-800 truncate max-w-[120px]">
                      {user?.email?.split('@')[0] || 'User'}
                    </span>
                    <span className="text-xs text-green-600 truncate max-w-[120px]">
                      {user?.email}
                    </span>
                  </div>
                  <ChevronUp className="ml-auto w-4 h-4" />
                </SidebarMenuButton>
              </DropdownMenuTrigger>
              <DropdownMenuContent 
                side="top" 
                className="w-[--radix-popper-anchor-width]"
              >
                <DropdownMenuItem asChild>
                  <Link href="/profile" className="cursor-pointer">
                    <User className="w-4 h-4 mr-2" />
                    Profile
                  </Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href="/settings" className="cursor-pointer">
                    <Settings className="w-4 h-4 mr-2" />
                    Settings
                  </Link>
                </DropdownMenuItem>
                <DropdownMenuItem 
                  onClick={signOut}
                  className="cursor-pointer text-red-600 focus:text-red-600"
                >
                  <LogOut className="w-4 h-4 mr-2" />
                  Sign out
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  )
}
