/** @type {import('next').NextConfig} */
const nextConfig = {
  // output: 'standalone' - desactivado para Vercel (causaba 404 en assets)
  reactStrictMode: true,
  experimental: {},
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': __dirname,
    }
    return config
  },
}

module.exports = nextConfig
