/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        cosmic: {
          950: "#080711",
          900: "#0d1020",
          800: "#121833",
          700: "#1b2147",
        },
        glow: {
          violet: "#8b7cff",
          indigo: "#5f77ff",
          gold: "#d7b977",
          moon: "#ece6ff",
        },
      },
      boxShadow: {
        aura: "0 24px 60px rgba(3, 4, 18, 0.45)",
        card: "0 18px 40px rgba(10, 12, 26, 0.42)",
      },
      fontFamily: {
        display: ["ui-serif", "Cambria", "Times New Roman", "Georgia", "serif"],
        sans: ["Inter", "Segoe UI", "system-ui", "sans-serif"],
      },
      backgroundImage: {
        cosmos:
          "radial-gradient(circle at 16% 18%, rgba(139,124,255,0.20), transparent 26%), radial-gradient(circle at 82% 12%, rgba(215,185,119,0.14), transparent 18%), radial-gradient(circle at 72% 72%, rgba(95,119,255,0.16), transparent 22%), linear-gradient(160deg, #080711 0%, #0d1020 48%, #121833 100%)",
      },
    },
  },
  plugins: [],
};
