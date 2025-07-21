import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Toaster } from 'react-hot-toast'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Podcastify - PDF to Audio Converter',
  description: 'Transform your PDF books into beautiful audio podcasts using AI',
  keywords: ['PDF', 'audio', 'podcast', 'TTS', 'AI', 'audiobook'],
  authors: [{ name: 'Podcastify Team' }],
  viewport: 'width=device-width, initial-scale=1',
  themeColor: '#6366F1',
  openGraph: {
    title: 'Podcastify - PDF to Audio Converter',
    description: 'Transform your PDF books into beautiful audio podcasts using AI',
    type: 'website',
    locale: 'en_US',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Podcastify - PDF to Audio Converter',
    description: 'Transform your PDF books into beautiful audio podcasts using AI',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-gradient-to-br from-pastel-blue via-pastel-purple to-pastel-pink">
          {children}
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: 'rgba(255, 255, 255, 0.9)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                borderRadius: '12px',
                color: '#374151',
              },
              success: {
                iconTheme: {
                  primary: '#10B981',
                  secondary: '#FFFFFF',
                },
              },
              error: {
                iconTheme: {
                  primary: '#EF4444',
                  secondary: '#FFFFFF',
                },
              },
            }}
          />
        </div>
      </body>
    </html>
  )
}
