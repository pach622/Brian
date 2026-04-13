/** @type {import('tailwindcss').Config} */

const defaultTheme = require('tailwindcss/defaultTheme');

module.exports = {
  // content: [ './src/pages/**/*.{js,ts,jsx,tsx}', './src/components/**/*.{js,ts,jsx,tsx}', './app/**/*.{js,ts,jsx,tsx}', ],
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        'primary-dark': '#070919',
        'primary-dark-text': '#1a202c',
        'primary-light': '#edf2f7',
        'accent-start': '#7c3aed',
        'accent-mid': '#6366f1',
        'accent-end': '#3b82f6',
      },
      fontFamily: {
        sans: ['Inter', ...defaultTheme.fontFamily.sans],
      },
      backgroundImage: {
        'gradient-accent': 'linear-gradient(135deg, #7c3aed, #6366f1, #3b82f6)',
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
  darkMode: 'class',
};
