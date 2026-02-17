/** @type {import('next').NextConfig} */
const nextConfig = {
  // output: 'standalone' - desactivado para Vercel (causaba 404 en assets)
  reactStrictMode: true,
  experimental: {},
}

module.exports = nextConfig
