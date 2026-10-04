/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#07101f',
        slatepanel: '#0f172a',
        aurora: '#67e8f9',
        signal: '#34d399',
        warning: '#fbbf24',
        danger: '#f87171',
      },
      boxShadow: {
        panel: '0 24px 80px rgba(6, 10, 24, 0.45)',
      },
    },
  },
  plugins: [],
}
