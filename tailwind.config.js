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
        backgroundcolor: "#EBD7C1",
        maingreen: '#1D8145',
        accentgreen: '#8CFF98',
        darkgreen: '#152614',
        brownsugar: '#BB7E5D',
      },
      dropShadow: {
        'accentgreen': '0 35px 35px rgb(140, 255, 152, 0.25)',
      },
    },
  },
  plugins: [],
}