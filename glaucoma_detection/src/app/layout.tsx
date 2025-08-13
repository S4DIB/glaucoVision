import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Glaucoma Detection AI - Advanced Retinal Analysis',
  description: 'Professional glaucoma detection system using deep learning and clinical data fusion for accurate retinal fundus analysis.',
  keywords: 'glaucoma detection, retinal analysis, AI diagnosis, ophthalmology, deep learning, fundus imaging',
  authors: [{ name: 'Glaucoma Detection AI Team' }],
  viewport: 'width=device-width, initial-scale=1',
  robots: 'index, follow',
  openGraph: {
    title: 'Glaucoma Detection AI - Advanced Retinal Analysis',
    description: 'Professional glaucoma detection system using deep learning and clinical data fusion for accurate retinal fundus analysis.',
    type: 'website',
    locale: 'en_US',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <head>
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
        <meta name="theme-color" content="#3b82f6" />
      </head>
      <body className={`${inter.className} antialiased`}>
        {children}
      </body>
    </html>
  )
}
