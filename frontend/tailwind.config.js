/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{svelte,html}", "./index.html"],
  theme: {
    extend: {
      colors: {
        "les-gray": "#373737",
        "les-blue": "#1565c0",
        "les-red": "#f23f44",
        "les-bg": "#1e1e2d",
        "les-frame": "#dadada",
      },
      transitionProperty: {
        width: "width",
      },
    },
  },
  plugins: [],
};
