/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#12051f",
        mist: "#f6edff",
        signal: "#29d8ff",
        ember: "#ff7ab6",
        ocean: "#7f5cff",
        neon: "#ff45c7",
        sunset: "#ff8b5f"
      },
      boxShadow: {
        panel: "0 18px 60px rgba(13, 4, 30, 0.45)",
        glow: "0 0 60px rgba(255, 69, 199, 0.35)"
      }
    }
  },
  plugins: []
};
