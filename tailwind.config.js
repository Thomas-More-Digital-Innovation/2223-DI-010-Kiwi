/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./keyTracker/templates/keyTracker/*.html",
    "./keyTracker/templates/keyTracker/components/*.html",
  ],
  theme:
  {
    extend: {
      colors: {
        backgroundgreen: '#75a181',
      },
    },
  },
  plugins: [],
}
