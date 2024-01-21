<script lang="ts">
  import {
    stepperData,
    efficiencyresultstore,
    type EfficiencyResult,
    isStarted,
  } from "./lib/stores";
  import { OpenAPI, SimulateService } from "./lib/client";

  import Stepper from "./components/stepper.svelte";
  import BaseLayout from "./components/baseLayout.svelte";

  OpenAPI.BASE = "http://localhost:8000";

  async function fetchData(chunkoffset = 0) {
    if (!$isStarted) return;
    if (chunkoffset === 308) {
      chunkoffset = 303;
      return;
    }
    try {
      const response = await SimulateService.planApiSimulatePlanPost({
        chunkoffset: chunkoffset,
        costmodel: $stepperData.costmodel,
        algorithm: $stepperData.algorithm,
        twinworld: $stepperData.twinworld,
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
      stepperData.update(data => {
        return {
          ...data,
          households: data.households
        };
      });
      efficiencyresultstore.update((store) => [...store, ...transformedResults]);
      setTimeout(() => fetchData(chunkoffset + 7), 50);
    } catch (err) {
      console.error("Error fetching data:", err);
      if (err.status !== 500) {
        return;
      } else {
        console.error("Server error:", err);
      }
    }
  }

  $: if ($isStarted) {
    fetchData();
  }

  // $: $isStarted && fetchData();
</script>

{#if $stepperData.households.length !== 0}
  <BaseLayout />
{:else}
  <Stepper />
{/if}
