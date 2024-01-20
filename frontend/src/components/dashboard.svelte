<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import Chart from "chart.js/auto";
  import { efficiencyresultstore } from "../lib/stores";

  let chartContainers = [];
  let charts = [];
  const maxDataPoints = 51;

  $: if ($efficiencyresultstore.length > 0) {
    updateCharts($efficiencyresultstore);
  }

  onMount(() => {
    initializeCharts();
    updateCharts($efficiencyresultstore);
  });

  onDestroy(() => {
    charts.forEach((chart) => chart?.destroy());
  });

  function initializeCharts() {
    chartContainers.forEach((container, index) => {
      charts[index] = new Chart(container.getContext("2d"), {
        type: "line",
        data: {
          labels: [],
          datasets: [{
            label: getChartLabel(index),
            data: [],
            backgroundColor: getChartColor(index),
            borderColor: getChartColor(index),
            fill: false,
          }],
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });
    });
  }

  function updateCharts(data) {
    console.log("Updating charts with mapped data:", data);
    charts.forEach((chart, index) => {
      const latestData = data.slice(-maxDataPoints);

      chart.data.labels = latestData.map((_, i) => `Data ${data.length - maxDataPoints + i + 1}`);
      chart.data.datasets[0].data = latestData.map(item => {
        switch (index) {
          case 0: return item.solarEnergyIndividual;
          case 1: return item.solarEnergyTotal;
          case 2: return item.internalBoughtEnergyPrice;
          case 3: return item.totalAmountSaved;
        }
      });
      console.log(`Chart ${index} data:`, chart.data.datasets[0].data);
      chart.update();
    });
  }

  function getChartLabel(index) {
    switch (index) {
      case 0: return "% Solar Energy (Individual)";
      case 1: return "% Solar Energy (Total)";
      case 2: return "Internal Bought Energy Price";
      case 3: return "Total Amount Saved";
    }
  }

  function getChartColor(index) {
    const colors = ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0"];
    return colors[index] || "#000000";
  }
</script>

{#each Array(4) as _, index (index)}
  <canvas bind:this={chartContainers[index]}></canvas>
{/each}
