'use client'

import { useAuth } from '@/components/AuthProvider'
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
  ChevronUp,
  Plug,
  MessageCircle
} from 'lucide-react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

const navigation = [
  {
    title: 'Main',
    items: [
      { title: 'Dashboard', url: '/dashboard', icon: Home },
      { title: 'Chat', url: '/chat', icon: MessageCircle },
      { title: 'Analytics', url: '/analytics', icon: BarChart3 },
      { title: 'Reports', url: '/reports', icon: FileText },
    ],
  },
  {
    title: 'Integrations',
    items: [
      { title: 'Connect Apps', url: '/integrations', icon: Plug },
    ],
  },
  // {
  //   title: 'Account',
  //   items: [
  //     { title: 'Profile', url: '/profile', icon: User },
  //     { title: 'Settings', url: '/settings', icon: Settings },
  //     { title: 'Help', url: '/help', icon: HelpCircle },
  //   ],
  // },
]

export function AppSidebar() {
  const { user, signOut } = useAuth()
  const pathname = usePathname()

  const getUserInitials = (email?: string) => {
    if (!email) return 'U'
    return email.charAt(0).toUpperCase()
  }

  return (
    <Sidebar className="border-gray-200">
      <SidebarHeader className="border-b border-gray-100">
        <div className="flex items-center gap-2 px-4 py-2">
          <img className='rounded-lg' src="/logo.png" alt="Rockefeller" width={64} height={64} />
        </div>
      </SidebarHeader>
      
      <SidebarContent>
        {navigation.map((group) => (
          <SidebarGroup key={group.title}>
            <SidebarGroupLabel className="text-gray-700">{group.title}</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {group.items.map((item) => (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton
                      asChild
                      isActive={pathname === item.url}
                      className="data-[active=true]:bg-gray-100 data-[active=true]:text-gray-800 hover:bg-gray-50 hover:text-gray-700"
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
      
      <SidebarFooter className="border-t border-gray-100">
        <SidebarMenu>
          <SidebarMenuItem>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <SidebarMenuButton className="hover:bg-gray-50">
                  <Avatar className="w-6 h-6">
                    <AvatarFallback className="bg-gray-100 text-gray-700 text-xs">
                      {getUserInitials(user?.email)}
                    </AvatarFallback>
                  </Avatar>
                  <div className="flex flex-col items-start text-left">
                    <span className="text-sm font-medium text-gray-900 truncate max-w-[120px]">
                      {user?.email?.split('@')[0] || 'User'}
                    </span>
                    <span className="text-xs text-gray-600 truncate max-w-[120px]">
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
