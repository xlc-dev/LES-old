<script lang="ts">
  /*
  The dashboard component contains all the relevant data that is created for the simulation
  that is run using the selected of created twin world, cost model, and algorithm for the
  current session. This component consists of graphs that are updated in realtime and other
  visualisations of the live data that the application collects and generates.
  */
  import { Chart } from "svelte-chartjs";

  import { onMount, onDestroy } from "svelte";
  import Chart from "chart.js/auto";
  import { writable } from "svelte/store";

  let chartContainer;
  let chart;

  let data = {
    labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
    datasets: [
      {
        label: "# of Votes",
        data: [12, 19, 3, 5, 2, 3],
        backgroundColor: [
          "rgba(255, 99, 132, 0.2)",
          "rgba(54, 162, 235, 0.2)",
          "rgba(255, 206, 86, 0.2)",
          "rgba(75, 192, 192, 0.2)",
          "rgba(153, 102, 255, 0.2)",
          "rgba(255, 159, 64, 0.2)",
        ],
        borderColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(153, 102, 255, 1)",
          "rgba(255, 159, 64, 1)",
        ],
        borderWidth: 1,
      },
    ],
  };

  let options = {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  onMount(() => {
    if (chartContainer) {
      chart = new Chart(chartContainer.getContext("2d"), {
        type: "bar",
        data: data,
        options: options,
      });
    }
  });

  onDestroy(() => {
    if (chart) {
      chart.destroy();
    }
  });
</script>

<canvas bind:this={chartContainer}></canvas>
