<script lang="ts">
  /*
   * The result component contains the end view that is displayed when the application determines
   * that the session has ended or if the researcher manually ends the session by pressing the
   * Stop Simulation button in the sidebar. This component takes a snapshot of all the data that
   * the application has gathered during the session and provides the researcher a way to display
   * and download this data before a new session is started.
   */

  import { onMount } from "svelte";

  import Chart from "./chart.svelte";

  import {
    stepperData,
    activatedHousehold,
    runtime,
    isStarted,
    efficiencyresultstore,
  } from "../lib/stores";

  import Stepper from "./stepper.svelte";
  import BaseLayout from "./baseLayout.svelte";

  let newSession = false;

  onMount(() => {
    $isStarted = false;
    runtime.stop();
  });

  function doNothing() {}

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
          on:click={doNothing}>Download</button>
      </div>
    </div>
  </div>
{:else if $stepperData.households.length !== 0}
  <BaseLayout />
{:else}
  <Stepper />
{/if}
