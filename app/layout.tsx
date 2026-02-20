import type { Metadata } from "next"
import { Inter, Source_Serif_4, JetBrains_Mono } from "next/font/google"
import "./globals.css"

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
})

const sourceSerif = Source_Serif_4({
  subsets: ["latin"],
  variable: "--font-serif",
})

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
})

export const metadata: Metadata = {
  title: "Dashboard de Entrenamientos - Polar RCX5",
  description: "Visualiza y analiza tus entrenamientos del Polar RCX5",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="es" className="dark">
      <body className={`${inter.variable} ${sourceSerif.variable} ${jetbrainsMono.variable} font-sans theme`}>
        {children}
      </body>
    </html>
  )
}
