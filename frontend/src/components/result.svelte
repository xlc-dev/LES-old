<script lang="ts">
  /*
  The result component contains the end view that is displayed when the application determines
  that the session has ended or if the researcher manually ends the session by pressing the
  Stop Simulation button in the sidebar. This component takes a snapshot of all the data that
  the application has gathered during the session and provides the researcher a way to display
  and download this data before a new session is started.
  */

  import { ApplianceDays, ApplianceType } from "../lib/client";
  import { Chart } from "svelte-chartjs";
  import "chart.js/auto";

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

  function refreshPage() {
    location.reload();
  }

  function doNothing() {
  }
</script>

<div class="max-w-3xl mx-auto pt-8">
  <div class="mt-8 bg-white rounded-lg p-4 mb-8 border-4 border-gray-400 shadow">
    <Chart type="bar" {data} {options} />
    <div class="buttons">
      <button on:click={refreshPage}>Refresh Page</button>
      <button on:click={doNothing}>Do Nothing</button>
    </div>
    <Chart type="bar" {data} {options} />
    <div class="buttons">
      <button on:click={refreshPage}>Refresh Page</button>
      <button on:click={doNothing}>Do Nothing</button>
    </div>
  </div>
</div>
