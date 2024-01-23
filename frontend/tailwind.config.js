const plugin = require("tailwindcss/plugin");

/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./src/**/*.svelte", "./index.html"],
  theme: {
    extend: {
      colors: {
        "les-blue": "#1565c0",
        "les-red": "#f23f44",
        "les-white": "#ffffff",
        "les-red-dark": "#610000",
        "les-highlight": "#2a2a3d",
        "les-table-cell": "#373737",
        "les-sort-inactive": "#838383",
        "les-sort-active": "#313131",
        "les-sidebar-item": "#12121b",

        "light-les-bg": "#1e1e2d",
        "light-les-frame": "#dadada",

        "dark-les-bg": "#22222c",
        "dark-les-frame": "#dadada",

        "dark-table-header": "#12121b",
        "dark-table-row": "#1a1a26",
        "dark-sidebar": "#111827",
      },
      transitionProperty: {
        width: "width",
      },
    },
  },
  plugins: [
    plugin(function ({ addBase, theme }) {
      addBase({
        "input[type='checkbox'], input[type='radio']": {
          cursor: "pointer",
          width: theme("width.4"),
          height: theme("height.4"),
          accentColor: theme("colors.les-highlight"),
        },
      });
    }),
  ],
};
