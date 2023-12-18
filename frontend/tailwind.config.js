/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{svelte,html}", "./index.html"],
  theme: {
    extend: {
      colors: {
        background: "#1e1e2d",
        "custom-gray": "#373737",
        "custom-blue": "#1565c0",
        "custom-red": "#f23f44",
        "les-bg": "#1e1e2d",
        "les-frame": "#dadada"
      },
      transitionProperty: {
        width: "width",
      },
    },
  },
  plugins: [],
};
