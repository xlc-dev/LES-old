<script lang="ts">
  /**
   * The App component is the root component of the application.
   * This component contains the logic that is responsible for fetching the simulation results from the API
   * And for displaying the stepper or the base layout depending on the state of the application.
   */

  import {
    stepperData,
    efficiencyresultstore,
    isStarted,
    runtime,
    timeDailies,
    startDate,
    endDate,
    messages,
    daysInPlanning,
  } from "./lib/stores";

  import { OpenAPI, SimulateService } from "./lib/client";

  import Stepper from "./components/stepper.svelte";
  import BaseLayout from "./components/baseLayout.svelte";
  import Message from "./components/message.svelte";
  import { message } from "./lib/message";

  OpenAPI.BASE = "http://localhost:8000";

  let showPopup = false;
  let fetchedData = false;

  /**
   * Fetches the simulation results from the API.
   * The API returns the results in chunks of 7 days.
   * This function is called recursively until the simulation is finished.
   * @param {number} chunkoffset - The offset of the chunk that is to be fetched.
   * @returns {void}
   */
  const fetchData = async (chunkoffset = 0) => {
    // Don't call the API if the simulation is not started
    if (!$isStarted) return;
    fetchedData = true;

    try {
      const response = await SimulateService.planApiSimulatePlanPost({
        chunkoffset: chunkoffset,
        costmodel: $stepperData.costmodel,
        algorithm: $stepperData.algorithm,
        twinworld: $stepperData.twinworld,
        energyflow: $stepperData.energyflow,
        households: $stepperData.households,
      });

      const transformedResults = response.results.map((resultArray) => ({
        solarEnergyIndividual: resultArray[0],
        solarEnergyTotal: resultArray[1],
        internalBoughtEnergyPrice: resultArray[2],
        totalAmountSaved: resultArray[3],
      }));

      // Updates the number of households constantly
      // This may be redundant, as this value isn't supposed to change during a session
      stepperData.update((data) => {
        return {
          ...data,
          households: data.households,
        };
      });
      efficiencyresultstore.update((store) => [...store, ...transformedResults]);
      timeDailies.update((store) => [...store, ...response.timedaily]);
      $startDate = response.start_date;
      $endDate = response.end_date;
      $daysInPlanning = response.days_in_planning;

      setTimeout(() => {
        if (!$isStarted) return;
        fetchData(chunkoffset + 7);
      }),
        50;
    } catch (err) {
      if (err.status === 400) {
        message(err);
        $isStarted = false;
        return;
      }
      if (err.status !== 500) {
        message(err);
        $isStarted = false;
        return;
      } else {
        console.error("Server error:", err);
      }
    }
  };

  /**
   * Stops the polling of the API.
   */
  const stopPolling = () => {
    fetchedData = false;
    $isStarted = false;
  };

  $: if ($isStarted) {
    runtime.start();
    fetchData();
  } else {
    runtime.stop();
    $isStarted = false;
    if (fetchedData) {
      showPopup = true;
    }
  }
</script>

<div class="fixed right-4 top-4 flex flex-col gap-6">
  {#each $messages as message}
    <Message message={message.msg} id={message.id} />
  {/each}
</div>

{#if $stepperData.households.length !== 0}
  <BaseLayout on:stop={stopPolling} />

  {#if showPopup}
    <div class="fixed inset-0 z-50 flex items-center justify-center">
      <div class="absolute inset-0 bg-gray-900 opacity-75"></div>
      <div class="relative rounded-lg bg-white p-8 shadow-2xl dark:bg-les-gray-600">
        <h2 class="mb-4 text-2xl font-bold dark:text-white">Simulation finished</h2>
        <div class="flex justify-between">
          <button
            class="mt-4 rounded-lg bg-les-blue p-2 text-white transition duration-200 hover:brightness-110"
            on:click={() => (showPopup = false)}>
            Continue
          </button>
          <button
            class="mt-4 rounded-lg bg-les-blue p-2 text-white transition duration-200 hover:brightness-110"
            on:click={() => {
              showPopup = false;
              fetchedData = false;
              document.getElementById("stop-button").click();
            }}>
            View Result
          </button>
        </div>
      </div>
    </div>
  {/if}
{:else}
  <Stepper />
{/if}
