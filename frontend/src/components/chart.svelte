<script lang="ts">
  /**
   * Shared chart logic between result.svelte and dashboard.svelte
   */

  import { onMount, onDestroy } from "svelte";

  import Chart from "chart.js/auto";
  import zoomPlugin from "chartjs-plugin-zoom";

  import { efficiencyresultstore, type EfficiencyResult } from "../lib/stores";

  let chartContainers: HTMLCanvasElement[] = [];
  let charts: Chart[] = [];

  /**
   * Initialize chart instances with default configurations.
   */
  const initializeCharts = () => {
    chartContainers.forEach((container, index) => {
      charts[index] = new Chart(container.getContext("2d"), {
        type: "line",
        data: {
          labels: [],
          datasets: [
            {
              label: getChartLabel(index),
              data: [],
              backgroundColor: getChartFillColor(index),
              borderColor: getChartColor(index),
              fill: true,
            },
          ],
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                color: getAxisTextColor(),
              },
              title: {
                display: true,
                text: getYAxisChartLabel(index),
              },
            },
            x: {
              ticks: {
                color: getAxisTextColor(),
              },
            },
          },
          plugins: {
            legend: {
              onClick: () => {}, // Disable legend click
              onHover: () => {}, // Disable legend hover
              labels: {
                color: getAxisTextColor(),
              },
            },
            zoom: {
              zoom: {
                wheel: {
                  enabled: true,
                },
                pinch: {
                  enabled: true,
                },
                mode: "x",
              },
              pan: {
                enabled: true,
                mode: "x",
              },
            },
          },
        },
      });
    });
  };

  /**
   * Update chart data based on efficiency result data.
   * @param {EfficiencyResult[]} data - The efficiency result data.
   */
  export const updateCharts = (data: EfficiencyResult[]) => {
    charts.forEach((chart, index) => {
      const latestData = data;

      // Update chart labels and datasets
      chart.data.labels = latestData.map((_, i) => `Day ${i + 1}`);
      chart.data.datasets[0].data = latestData.map((item) => item[solarDataKeys[index]]);
      chart.update();
    });
  };

  // Keys corresponding to efficiency data properties
  const solarDataKeys: string[] = [
    "solarEnergyIndividual",
    "solarEnergyTotal",
    "internalBoughtEnergyPrice",
    "totalAmountSaved",
  ];

  /**
   * Get the y axis label for the chart based on the chart index.
   * @param {number} index - The index of the chart.
   * @returns {string} - The chart label.
   */
  const getYAxisChartLabel = (index: number): string => {
    const labels: string[] = [
      "Fraction of solar energy used by houses themselves",
      "Fraction of solar energy used by all houses",
      "Price of internal energy (local currency)",
      "Money saved by community (local currency)",
    ];
    return labels[index] || "";
  };

  /**
   * Get the label for the chart based on the chart index.
   * @param {number} index - The index of the chart.
   * @returns {string} - The chart label.
   */
  const getChartLabel = (index: number): string => {
    const labels: string[] = [
      "% Solar Energy (Individual)",
      "% Solar Energy (Total)",
      "Internal Bought Energy Price",
      "Total Amount Saved",
    ];
    return labels[index] || "";
  };

  /**
   * Get the fill color for the chart based on the chart index.
   * @param {number} index - The index of the chart.
   * @returns {string} - The fill color.
   */
  const getChartFillColor = (index: number): string =>
    getColor(index, [
      "rgba(255, 0, 0, 0.2)",
      "rgba(255, 255, 0, 0.2)",
      "rgba(0, 0, 255, 0.2)",
      "rgba(0, 128, 0, 0.2)",
    ]);

  /**
   * Get the border color for the chart based on the chart index.
   * @param {number} index - The index of the chart.
   * @returns {string} - The border color.
   */
  const getChartColor = (index: number): string =>
    getColor(index, ["#f23f44", "#cbba07", "#1565c0", "#15803d"]);

  /**
   * Get color from an array or provide a default if not present.
   * @param {number} index - The index to access in the array.
   * @param {string[]} array - The array of colors.
   * @returns {string} - The color at the specified index.
   */
  const getColor = (index: number, array: string[]): string => array[index];

  /**
   * Get the axis text color based on Tailwind CSS dark mode.
   * @returns {string} - The axis text color.
   */
  const getAxisTextColor = (): string => (darkModeEnabled() ? "#FFFFFF" : "#000000");

  /**
   * Check if Tailwind CSS dark mode is enabled.
   * @returns {boolean} - True if dark mode is enabled, false otherwise.
   */
  const darkModeEnabled = (): boolean => localStorage.getItem("darkMode") === "true";

  // Listen for dark mode changes
  const observer = new MutationObserver((mutationsList) => {
    for (const mutation of mutationsList) {
      if (mutation.type === "attributes" && mutation.attributeName === "class") {
        charts.forEach((chart) => {
          chart.options.scales.y.ticks.color = getAxisTextColor();
          chart.options.scales.x.ticks.color = getAxisTextColor();
          chart.options.plugins.legend.labels.color = getAxisTextColor();
          chart.update();
        });
      }
    }
  });

  /*
   * Contains logic that runs at initialisation, as soon as the component has been mounted.
   * In this component it initialises the (state of the) graphs.
   */
  onMount(() => {
    initializeCharts();
    updateCharts($efficiencyresultstore);
    Chart.register(zoomPlugin);
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });
  });

  /*
   * Contains logic that runs immediately before the component is unmounted.
   * In this component it destroys the charts.
   */
  onDestroy(() => {
    charts.forEach((chart) => chart?.destroy());
    observer.disconnect();
  });

  // Update charts when efficiency result store has data
  $: $efficiencyresultstore.length && updateCharts($efficiencyresultstore);
</script>

<div class="grid grid-cols-2 gap-4 rounded-lg bg-white p-4 dark:bg-les-gray-600">
  {#each Array(4) as _, index (index)}
    <div>
      <canvas bind:this={chartContainers[index]}></canvas>
    </div>
  {/each}
</div>
