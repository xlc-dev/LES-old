const plugin = require("tailwindcss/plugin");

/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./src/**/*.svelte", "./index.html"],
  theme: {
    extend: {
      colors: {
        "les-gray": {
          50: "#f4f9fb",
          100: "#edf5f8",
          200: "#dadada",
          300: "#838383",
          400: "#313131",
          500: "#22222c",
          600: "#1a1a26",
          700: "#12121b",
        },
        "les-blue": "#1565c0",
        "les-red": "#f23f44",
        "les-white": "#ffffff",
        "les-red-dark": "#610000",
        "les-highlight": "#2a2a3d",
        "les-dark-date-picker-text": "#0e8bf8",
        sidebar: "#111827",
      },
      transitionProperty: {
        width: "width",
      },
    },
  },
  plugins: [
    plugin(function ({ addBase, addComponents, theme }) {
      addBase({
        "input[type='checkbox'], input[type='radio']": {
          cursor: "pointer",
          width: theme("width.4"),
          height: theme("height.4"),
          accentColor: theme("colors.les-highlight"),
        },
      });
      addComponents({
        ".calendar": {
          "--date-picker-foreground": theme("colors.les-highlight"),
          "--date-picker-background": theme("colors.les-white"),
          "--date-picker-highlight-border": theme("colors.les-blue"),
          "--date-picker-highlight-shadow": theme("colors.les-highlight"),
          "--date-picker-selected-color": theme("colors.les-white"),
          "--date-picker-selected-background": theme("colors.les-blue"),
        },
        ".calendar-dark": {
          "--date-picker-foreground": theme("colors.les-dark-date-picker-text"),
          "--date-picker-background": theme("colors.les-gray.500"),
          "--date-picker-highlight-border": theme("colors.les-blue"),
          "--date-picker-highlight-shadow": theme("colors.les-gray.700"),
          "--date-picker-selected-color": theme("colors.les-dark"),
          "--date-picker-selected-background": theme("colors.les-blue"),
        },
      });
    }),
  ],
};
