import { NextRequest, NextResponse } from 'next/server'
import puppeteer from 'puppeteer'

export async function POST(req: NextRequest) {
  try {
    const { deckId, slides } = await req.json()

    if (!deckId || !slides) {
      return NextResponse.json({ error: 'Missing required parameters' }, { status: 400 })
    }

    // Launch Puppeteer
    const browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    })

    const page = await browser.newPage()
    
    // Set viewport for consistent rendering
    await page.setViewport({ width: 1920, height: 1080 })

    // Generate HTML for the pitch deck
    const html = generatePitchDeckHTML(slides)
    
    // Set the HTML content
    await page.setContent(html, { waitUntil: 'networkidle0' })

    // Generate PDF
    const pdf = await page.pdf({
      format: 'A4',
      landscape: true,
      printBackground: true,
      margin: {
        top: '0.5in',
        right: '0.5in',
        bottom: '0.5in',
        left: '0.5in'
      }
    })

    await browser.close()

    // Return PDF as response
    return new NextResponse(Buffer.from(pdf), {
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': `attachment; filename="pitch-deck-${deckId}.pdf"`
      }
    })

  } catch (error) {
    console.error('PDF generation error:', error)
    return NextResponse.json({ error: 'Failed to generate PDF' }, { status: 500 })
  }
}

function generatePitchDeckHTML(slides: any[]) {
  return `
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Pitch Deck</title>
      <style>
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }
        
        body {
          font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
          background: #f8fafc;
        }
        
        .slide {
          width: 100vw;
          height: 100vh;
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          padding: 80px;
          page-break-after: always;
          background: white;
        }
        
        .slide:last-child {
          page-break-after: avoid;
        }
        
        .slide-icon {
          font-size: 4rem;
          margin-bottom: 2rem;
        }
        
        .slide-title {
          font-size: 3rem;
          font-weight: bold;
          color: #1e293b;
          margin-bottom: 3rem;
          text-align: center;
        }
        
        .slide-content {
          max-width: 1000px;
          width: 100%;
        }
        
        .slide-point {
          display: flex;
          align-items: flex-start;
          gap: 1rem;
          margin-bottom: 1.5rem;
          font-size: 1.5rem;
          line-height: 1.6;
          color: #475569;
        }
        
        .slide-point::before {
          content: '•';
          color: #3b82f6;
          font-weight: bold;
          font-size: 2rem;
          line-height: 1;
          margin-top: 0.2rem;
        }
        
        .slide-number {
          position: absolute;
          bottom: 2rem;
          right: 2rem;
          font-size: 1rem;
          color: #64748b;
        }
        
        .title-slide {
          background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
          color: white;
        }
        
        .title-slide .slide-title {
          color: white;
          font-size: 4rem;
        }
        
        .title-slide .slide-point {
          color: #e2e8f0;
          font-size: 1.8rem;
        }
        
        .title-slide .slide-point::before {
          color: #fbbf24;
        }
      </style>
    </head>
    <body>
      ${slides.map((slide, index) => `
        <div class="slide ${index === 0 ? 'title-slide' : ''}">
          <div class="slide-icon">${slide.icon || '📊'}</div>
          <h1 class="slide-title">${slide.title}</h1>
          <div class="slide-content">
            ${Array.isArray(slide.content)
              ? slide.content.map((point: any) => `
                  <div class="slide-point">${String(point)}</div>
                `).join('')
              : `<div class=\"slide-point\">${String(slide.content ?? '')}</div>`}
          </div>
          <div class="slide-number">${index + 1} / ${slides.length}</div>
        </div>
      `).join('')}
    </body>
    </html>
  `
}
