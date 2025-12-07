/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class", // Ensure dark mode strategy is set
  theme: {
    extend: {
      colors: {
        "primary": "#dc2626",
        "secondary": "#f8f9fa",
        "accent": "#dc2626",
        
        // Backgrounds
        "background-light": "#f8fafc", // Updated to Slate-50 for Analytics
        "background-dark": "#0f172a",  // Updated to Slate-900 for Analytics
        
        // Surfaces
        "surface-light": "#ffffff",
        "surface-dark": "#1e293b", // Slate-800

        // Text
        "text-light": "#1e293b", // Slate-800
        "text-dark": "#f8fafc", // Slate-50
        "text-muted-light": "#64748b", // Slate-500
        "text-muted-dark": "#94a3b8", // Slate-400
        
        // Borders
        "border-light": "#e2e8f0", // Slate-200
        "border-dark": "#334155", // Slate-700
      },
      fontFamily: {
        sans: ['Lexend', 'sans-serif'],
        display: ['Lexend', 'sans-serif'],
        poppins: ['Poppins', 'sans-serif'], // Added for Analytics Page
      },
    },
  },
  plugins: [],
}