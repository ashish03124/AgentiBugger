import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Agentic Bug Hunter | Premium Code Analysis',
  description: 'AI-powered pipeline for semiconductor code bug detection.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <div className="bg-mesh" />
        {children}
      </body>
    </html>
  )
}
