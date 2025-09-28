import { NextRequest, NextResponse } from 'next/server'
import { createServerClient } from '@/lib/supabase-server'

export async function POST(req: NextRequest) {
  try {
    const { pdfBuffer, fileName } = await req.json()

    if (!pdfBuffer || !fileName) {
      return NextResponse.json({ error: 'Missing required parameters' }, { status: 400 })
    }

    // Convert base64 to buffer if needed
    let buffer: Buffer
    if (typeof pdfBuffer === 'string') {
      // It's base64 encoded
      buffer = Buffer.from(pdfBuffer, 'base64')
    } else {
      // It's already a buffer
      buffer = Buffer.from(pdfBuffer)
    }

    // Upload to Supabase Storage
    const supabase = createServerClient()
    const filePath = `pitch-decks/${fileName}`
    
    const { error } = await supabase.storage
      .from('product_images')
      .upload(filePath, buffer, {
        contentType: 'application/pdf',
        upsert: true
      })
    
    if (error) {
      console.error('Error uploading pitch deck to Supabase:', error)
      return NextResponse.json({ error: 'Failed to upload PDF' }, { status: 500 })
    }

    // Get public URL
    const { data: urlData } = supabase.storage
      .from('product_images')
      .getPublicUrl(filePath)

    return NextResponse.json({ 
      success: true, 
      pdf_url: urlData.publicUrl 
    })

  } catch (error) {
    console.error('PDF upload error:', error)
    return NextResponse.json({ error: 'Failed to upload PDF' }, { status: 500 })
  }
}
