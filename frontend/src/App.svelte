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
      if (err.status !== 500) {
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

<div class="flex flex-col gap-6 fixed top-4 right-4">
  {#each $messages as message}
    <Message message={message.msg} id={message.id} />
  {/each}
</div>

{#if $stepperData.households.length !== 0}
  <BaseLayout on:stop={stopPolling} />

  {#if showPopup}
    <div class="fixed inset-0 flex items-center justify-center z-50">
      <div class="absolute bg-gray-900 opacity-75 inset-0"></div>
      <div class="relative bg-white dark:bg-dark-table-row p-8 rounded-lg shadow-2xl">
        <h2 class="text-2xl font-bold mb-4 dark:text-white">Simulation finished</h2>
        <div class="flex justify-between">
          <button
            class="mt-4 p-2 bg-les-blue hover:brightness-110 transition duration-200 text-white rounded-lg"
            on:click={() => (showPopup = false)}>
            Continue
          </button>
          <button
            class="mt-4 p-2 bg-les-blue hover:brightness-110 transition duration-200 text-white rounded-lg"
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
