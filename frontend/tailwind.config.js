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
          "--date-picker-foreground": theme("colors.les-white"),
          "--date-picker-background": theme("colors.dark-les-bg"),
          "--date-picker-highlight-border": theme("colors.les-blue"),
          "--date-picker-highlight-shadow": theme("colors.les-sidebar-item"),
          "--date-picker-selected-color": theme("colors.les-dark"),
          "--date-picker-selected-background": theme("colors.les-blue"),
        },
      });
    }),
  ],
};
