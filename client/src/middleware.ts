import { createMiddlewareClient } from '@supabase/auth-helpers-nextjs'
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(req: NextRequest) {
  const res = NextResponse.next()
  const supabase = createMiddlewareClient({ req, res })

  const {
    data: { user },
  } = await supabase.auth.getUser()

  const pathname = req.nextUrl.pathname

  // Allow access to login page for unauthenticated users
  if (pathname === '/login') {
    return res
  }

  // Allow access to root path for both authenticated and unauthenticated users
  if (pathname === '/') {
    return res
  }

  // If user is not signed in, redirect to /login
  if (!user) {
    return NextResponse.redirect(new URL('/login', req.url))
  }

  return res
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - auth (auth callback routes)
     */
    '/((?!api|_next/static|_next/image|favicon.ico|auth|.*\\.).*)',
  ],
}
