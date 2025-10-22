/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./main_app/templates/**/*.html",
    "./main_app/**/*.html",
    "./templates/**/*.html",
    "./**/*.html",
  ],
  safelist: [ // to ensure these classes are not purged
    'bg-gradient-to-br',
    'from-purple-500',
    'via-pink-500',
    'to-yellow-300',
    'min-h-screen',
    'flex',
    'items-center',
    'justify-center',
  ],
  theme: { extend: {} },
  plugins: [],
}
