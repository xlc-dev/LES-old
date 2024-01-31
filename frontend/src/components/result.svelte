<script lang="ts">
  /*
   * The result component contains the end view that is displayed when the application determines
   * that the session has ended or if the researcher manually ends the session by pressing the
   * Stop Simulation button in the sidebar. This component takes a snapshot of all the data that
   * the application has gathered during the session and provides the researcher a way to display
   * and download this data before a new session is started.
   */

  import { onMount } from "svelte";
  import * as XLSX from "xlsx";

  import {
    stepperData,
    activatedHousehold,
    runtime,
    isStarted,
    timeDailies,
    efficiencyresultstore,
  } from "../lib/stores";

  import BaseLayout from "./baseLayout.svelte";
  import Chart from "./chart.svelte";
  import Stepper from "./stepper.svelte";

  let newSession = false;

  const s2ab = (s) => {
    const buffer = new ArrayBuffer(s.length);
    const view = new Uint8Array(buffer);
    for (let i = 0; i < s.length; i++) {
      view[i] = s.charCodeAt(i) & 0xff;
    }
    return buffer;
  };

  const getGraphData = () => {
    const efficiencyResults = $efficiencyresultstore;
    let graphData = {
      graph1: [],
      graph2: [],
      graph3: [],
      graph4: [],
    };

    efficiencyResults.forEach((result, index) => {
      const dayNumber = index + 1;
      graphData.graph1.push(
        `internalBoughtEnergyPrice x: Day ${dayNumber}, y: ${result.internalBoughtEnergyPrice}`
      );
      graphData.graph2.push(
        `solarEnergyIndividual x: Day ${dayNumber}, y: ${result.solarEnergyIndividual}`
      );
      graphData.graph3.push(`solarEnergyTotal x: Day ${dayNumber}, y: ${result.solarEnergyTotal}`);
      graphData.graph4.push(`totalAmountSaved x: Day ${dayNumber}, y: ${result.totalAmountSaved}`);
    });
    return graphData;
  };

  const processGraphDataAndAddToWorkbook = (graphData, workbook) => {
    Object.keys(graphData).forEach((graphKey) => {
      const graphPoints = graphData[graphKey].map((point) => {
        const [xPart, yPart] = point.split(",");
        return {
          X: xPart.split(":")[1].trim(),
          Y: yPart.split(":")[1].trim(),
        };
      });
      XLSX.utils.book_append_sheet(workbook, XLSX.utils.json_to_sheet(graphPoints), graphKey);
    });
  };

  const getDashboardData = () => {
    const stepperDataValue = $stepperData;
    const efficiencyResults = $efficiencyresultstore;

    let sumEfficiencyIndividual = efficiencyResults.reduce(
      (acc, result) => acc + result.solarEnergyIndividual,
      0
    );
    let sumEfficiencyTotal = efficiencyResults.reduce(
      (acc, result) => acc + result.solarEnergyTotal,
      0
    );
    let sumTotalMoneySaved = efficiencyResults.reduce(
      (acc, result) => acc + result.totalAmountSaved,
      0
    );
    let sumEfficiencyNoSolar = sumEfficiencyTotal - sumEfficiencyIndividual;

    return [
      { label: "Number of Households", value: stepperDataValue.households.length },
      {
        label: "Cost Model Price Network Buy Consumer",
        value: stepperDataValue.costmodel.price_network_buy_consumer,
      },
      {
        label: "Cost Model Price Network Sell Consumer",
        value: stepperDataValue.costmodel.price_network_sell_consumer,
      },
      {
        label: "Twin World Energy Usage Factor",
        value: stepperDataValue.twinworld.energy_usage_factor,
      },
      {
        label: "Twin World Solar Panels Factor",
        value: stepperDataValue.twinworld.solar_panels_factor,
      },
      { label: "Algorithm Max Temperature", value: stepperDataValue.algorithm.max_temperature },
      {
        label: "Total Saved by Own Solar Panels",
        value: `${sumEfficiencyIndividual.toFixed(2)} kWh`,
      },
      {
        label: "Total Saved by Other Households' Solar Panels",
        value: `${sumEfficiencyNoSolar.toFixed(2)} kWh`,
      },
      { label: "Total Saved by the Community", value: `${sumEfficiencyTotal.toFixed(2)} kWh` },
      { label: "Total Money Saved", value: `€${sumTotalMoneySaved.toFixed(2)}` },
      { label: "Runtime", value: `${$runtime} seconds` },
      { label: "Selected Twin World", value: stepperDataValue.twinworld.name },
      { label: "Selected Cost Model", value: stepperDataValue.costmodel.name },
      { label: "Selected Algorithm", value: stepperDataValue.algorithm.name },
    ];
  };

  export const downloadExcel = () => {
    const timeDailiesData = $timeDailies;
    const graphData = getGraphData();
    const dashboardData = getDashboardData();

    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(timeDailiesData), "Time Dailies");
    processGraphDataAndAddToWorkbook(graphData, wb);
    XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(dashboardData), "Dashboard Data");
    const wbout = XLSX.write(wb, { bookType: "xlsx", type: "binary" });
    const blob = new Blob([s2ab(wbout)], { type: "application/octet-stream" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "session-data.xlsx";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

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
  };

  /*
    Contains logic that runs at initialisation, as soon as the component has been mounted.
    In this component it stops the runtime count and modifies the state of the simulation.
   */
  onMount(() => {
    $isStarted = false;
    runtime.stop();
  });
</script>

{#if !newSession}
  <div class="max-w-3xl mx-auto pt-8">
    <Chart />
    <div
      class="mt-8 bg-white dark:bg-dark-table-row dark:text-white rounded-lg p-4 mb-8 shadow grid grid-cols-2 gap-4 relative">
      <p class="absolute left-1/2 transform -translate-x-1/2 mt-4">Runtime: {$runtime} seconds</p>
      <div class="col-span-2 flex justify-between mt-8">
        <button
          class="px-6 py-3 rounded-lg text-white transition-colors duration-200 bg-les-blue hover:brightness-110"
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
