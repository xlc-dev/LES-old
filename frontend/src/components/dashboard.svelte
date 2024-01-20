<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import Chart from "chart.js/auto";
  import { efficiencyresultstore } from "../lib/stores";

  let chartContainers = [];
  let charts = [];

  function setupCharts() {
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
    if (data.length === 0) return;

    charts.forEach((chart, index) => {
      chart.data.labels = data.map((_, i) => `Data ${i + 1}`);
      chart.data.datasets[0].data = data.map((r) => {
        switch (index) {
          case 0: return r.solarEnergyIndividual;
          case 1: return r.solarEnergyTotal;
          case 2: return r.internalBoughtEnergyPrice;
          case 3: return r.totalAmountSaved;
        }
      });
      chart.update();
    });
  }

  onMount(() => {
    setupCharts();

    const unsubscribe = efficiencyresultstore.subscribe(updateCharts);

    onDestroy(() => {
      unsubscribe();
      charts.forEach((chart) => chart?.destroy());
    });
  });

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
