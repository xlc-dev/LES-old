<script lang="ts">
  /*
   * The result component contains the end view that is displayed when the application determines
   * that the session has ended or if the researcher manually ends the session by pressing the
   * Stop Simulation button in the sidebar. This component takes a snapshot of all the data that
   * the application has gathered during the session and provides the researcher a way to display
   * and download this data before a new session is started.
   */

  import { onMount } from "svelte";
  import { get } from 'svelte/store';
  import Chart from "./chart.svelte";
  import Papa from 'papaparse';

  import {
    stepperData,
    activatedHousehold,
    runtime,
    isStarted,
    timeDailies,
    efficiencyresultstore,
  } from "../lib/stores";

  import Stepper from "./stepper.svelte";
  import BaseLayout from "./baseLayout.svelte";

  let newSession = false;

  onMount(() => {
    $isStarted = false;
    runtime.stop();
  });

  const newSessionButton = () => {
    $stepperData = {
      algorithm: {} as any,
      twinworld: {} as any,
      costmodel: {} as any,
      households: [] as any[],
    };

    $activatedHousehold = null;
    $efficiencyresultstore = [];
    $runtime = 0;
    newSession = true;
  }

  function downloadCSV() {
    const timeDailiesData = get(timeDailies);
    const selectedOptions = get(stepperData);
    const graphData = getGraphData();
    const csvData = convertToCSV({ timeDailiesData, selectedOptions, graphData });
    triggerCSVDownload(csvData, 'session-data.csv');
  }

  function getGraphData() {
    return [];
  }

  function convertToCSV(data) {
    const { timeDailiesData, selectedOptions, graphData } = data;
    const csvData = [
      ["$timeDailies", "Selected Options", "Graph Data"],
      ...timeDailiesData.map((item, index) => [
        JSON.stringify(item),
        JSON.stringify(selectedOptions),
        JSON.stringify(graphData[index] || {})
      ])
    ];
    return Papa.unparse(csvData);
  }

  function triggerCSVDownload(csvData, filename) {
    const blob = new Blob([csvData], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
  }
</script>

{#if !newSession}
  <div class="max-w-3xl mx-auto pt-8">
    <Chart />
    <div
      class="mt-8 bg-white rounded-lg p-4 mb-8 border-4 border-gray-400 shadow grid grid-cols-2 gap-4 relative">
      <p class="absolute left-1/2 transform -translate-x-1/2 mt-4">Runtime: {$runtime} seconds</p>
      <div class="col-span-2 flex justify-between mt-8">
        <button
          class="px-6 py-3 rounded-lg text-white transition-colors duration-200 bg-les-highlight hover:bg-dark-les-bg"
          on:click={newSessionButton}>New session</button>
        <button
          class="px-6 py-3 rounded-lg text-white transition-colors duration-200 bg-les-blue hover:brightness-110"
          on:click={downloadCSV}>Download</button>
      </div>
    </div>
  </div>
{:else if $stepperData.households.length !== 0}
  <BaseLayout />
{:else}
  <Stepper />
{/if}
