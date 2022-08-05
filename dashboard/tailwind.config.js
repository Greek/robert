/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx}',
    './src/modules/**/*.{js,ts,tsx}',
    './src/ui/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: [
          'Inter',
          '-apple-system',
          'BlinkMacSystemFont',
          'Segoe UI',
          'Roboto',
          'Helvetica',
          'Arial',
          'sans-serif',
        ],
        mono: ['Menlo', 'Monaco', 'Courier New', 'monospace'],
      },
      colors: {
        button: 'var(--color-button-text)',
        'button-bg': 'var(--color-button-bg)',
        'layout-bg': 'var(--color-layout-bg)',
        'color-text': 'var(--color-text)',
      },
    },
  },
  plugins: [],
};
