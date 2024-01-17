<script lang="ts">
  /*
  The result component contains the end view that is displayed when the application determines
  that the session has ended or if the researcher manually ends the session by pressing the
  Stop Simulation button in the sidebar. This component takes a snapshot of all the data that
  the application has gathered during the session and provides the researcher a way to display
  and download this data before a new session is started.
  */

  import { onMount, onDestroy } from 'svelte';
  import Chart from 'chart.js/auto';
  import { writable } from 'svelte/store';

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
      chart = new Chart(chartContainer.getContext('2d'), {
        type: 'line',
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

  function refreshPage() {
    location.reload();
  }

  function doNothing() {
  }
</script>

<div class="max-w-3xl mx-auto pt-8">
  <div class="mt-8 bg-white rounded-lg p-4 mb-8 border-4 border-gray-400 shadow">
    <canvas bind:this={chartContainer}></canvas>
    <div class="buttons flex justify-between mt-8">
      <button class="px-6 py-3 rounded-lg text-white transition-colors duration-200 bg-les-highlight hover:bg-dark-les-bg" on:click={refreshPage}>New session</button>
      <button class="px-6 py-3 rounded-lg text-white transition-colors duration-200 bg-les-blue hover:brightness-110" on:click={doNothing}>Download</button>
    </div>
  </div>
</div>
