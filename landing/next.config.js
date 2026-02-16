/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  experimental: {},
  turbopack: {
    root: '..',
  },
}

module.exports = nextConfig
