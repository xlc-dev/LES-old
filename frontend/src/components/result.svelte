<script lang="ts">
  /*
  The result component contains the end view that is displayed when the application determines
  that the session has ended or if the researcher manually ends the session by pressing the
  Stop Simulation button in the sidebar. This component takes a snapshot of all the data that
  the application has gathered during the session and provides the researcher a way to display
  and download this data before a new session is started.
  */

  import { onMount, onDestroy } from "svelte";
  import Chart from "chart.js/auto";
  import { runtime } from "../lib/stores";

  let chartContainer;
  let chartContainerTwo;
  let chartContainerThree;
  let chartContainerFour;
  let chart;
  let chartTwo;
  let chartThree;
  let chartFour;

  let data = {
    labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
    datasets: [
      {
        label: "Energy produced",
        data: [14, 11, 17, 8, 12, 19],
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

  let dataTwo = {
    labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
    datasets: [
      {
        label: "Energy used",
        data: [15, 11, 7, 19, 12, 6],
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

  let dataThree = {
    labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
    datasets: [
      {
        label: "External energy from grid",
        data: [3, 6, 14, 8, 6, 2],
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

  let dataFour = {
    labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
    datasets: [
      {
        label: "Internal energy from solar panels",
        data: [6, 9, 12, 16, 18, 19],
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
        type: "line",
        data: data,
        options: options,
      });
    }
    if (chartContainerTwo) {
      chartTwo = new Chart(chartContainerTwo.getContext("2d"), {
        type: "bar",
        data: dataTwo,
        options: options,
      });
    }
    if (chartContainerThree) {
      chartThree = new Chart(chartContainerThree.getContext("2d"), {
        type: "line",
        data: dataThree,
        options: options,
      });
    }
    if (chartContainerFour) {
      chartFour = new Chart(chartContainerFour.getContext("2d"), {
        type: "bar",
        data: dataFour,
        options: options,
      });
    }
  });

  onDestroy(() => {
    if (chart) {
      chart.destroy();
    }
    if (chartTwo) {
      chartTwo.destroy();
    }
    if (chartThree) {
      chartThree.destroy();
    }
    if (chartFour) {
      chartFour.destroy();
    }
  });

  function refreshPage() {
    location.reload();
  }

  function doNothing() {}
</script>

<div class="max-w-3xl mx-auto pt-8">
  <div
    class="mt-8 bg-white rounded-lg p-4 mb-8 border-4 border-gray-400 shadow grid grid-cols-2 gap-4">
    <div class="chart-container">
      <canvas bind:this={chartContainer}></canvas>
    </div>
    <div class="chart-container">
      <canvas bind:this={chartContainerTwo}></canvas>
    </div>
    <div class="chart-container">
      <canvas bind:this={chartContainerThree}></canvas>
    </div>
    <div class="chart-container">
      <canvas bind:this={chartContainerFour}></canvas>
    </div>
    <p>Runtime: {$runtime} seconds</p>
    <div class="col-span-2 flex justify-between mt-8">
      <button
        class="px-6 py-3 rounded-lg text-white transition-colors duration-200 bg-les-highlight hover:bg-dark-les-bg"
        on:click={refreshPage}>New session</button>
      <button
        class="px-6 py-3 rounded-lg text-white transition-colors duration-200 bg-les-blue hover:brightness-110"
        on:click={doNothing}>Download</button>
    </div>
  </div>
</div>
