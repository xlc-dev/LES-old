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
  import * as XLSX from 'xlsx';
  import streamSaver from 'streamsaver';

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

  export function downloadExcel() {
    const timeDailiesData = get(timeDailies);
    const graphData = getGraphData();

    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(timeDailiesData), "Time Dailies");
    processGraphDataAndAddToWorkbook(graphData, wb);
    const wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'binary' });
    const blob = new Blob([s2ab(wbout)], { type: 'application/octet-stream' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'session-data.xlsx';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function processGraphDataAndAddToWorkbook(graphData, workbook) {
    Object.keys(graphData).forEach(graphKey => {
      const graphPoints = graphData[graphKey].map(point => {
        const [xPart, yPart] = point.split(',');
        return {
          X: xPart.split(':')[1].trim(),
          Y: yPart.split(':')[1].trim()
        };
      });
      XLSX.utils.book_append_sheet(workbook, XLSX.utils.json_to_sheet(graphPoints), graphKey);
    });
  }

  function s2ab(s) {
    const buffer = new ArrayBuffer(s.length);
    const view = new Uint8Array(buffer);
    for (let i = 0; i < s.length; i++) {
      view[i] = s.charCodeAt(i) & 0xFF;
    }
    return buffer;
  }

  function getGraphData() {
    const efficiencyResults = get(efficiencyresultstore);
    let graphData = {
      graph1: [],
      graph2: [],
      graph3: [],
      graph4: []
    };

    efficiencyResults.forEach((result, index) => {
      const dayNumber = index + 1;
      graphData.graph1.push(`internalBoughtEnergyPrice x: Day ${dayNumber}, y: ${result.internalBoughtEnergyPrice}`);
      graphData.graph2.push(`solarEnergyIndividual x: Day ${dayNumber}, y: ${result.solarEnergyIndividual}`);
      graphData.graph3.push(`solarEnergyTotal x: Day ${dayNumber}, y: ${result.solarEnergyTotal}`);
      graphData.graph4.push(`totalAmountSaved x: Day ${dayNumber}, y: ${result.totalAmountSaved}`);
    });
    return graphData;
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
          on:click={downloadExcel}>Download</button>
      </div>
    </div>
  </div>
{:else if $stepperData.households.length !== 0}
  <BaseLayout />
{:else}
  <Stepper />
{/if}
