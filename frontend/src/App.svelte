<script lang="ts">
  import { stepperData, efficiencyresultstore, type EfficiencyResult, isStarted } from "./lib/stores";
  import { OpenAPI, SimulateService } from "./lib/client";

  import Stepper from "./components/stepper.svelte";
  import BaseLayout from "./components/baseLayout.svelte";

  OpenAPI.BASE = "http://localhost:8000";

  // Recursive function to fetch data and update the store
  async function fetchData(chunkoffset = 0, previousSolarEnergyTotal = 0, previousTotalAmountSaved = 0) {
    try {
      const response = await SimulateService.planApiSimulatePlanPost({
        chunkoffset: chunkoffset,
        costmodel: $stepperData.costmodel,
        algorithm: $stepperData.algorithm,
        twinworld: $stepperData.twinworld,
        households: $stepperData.households,
      });

      // const transformedResults = response.results.map((resultArray, index) => {
      //   let solarEnergyTotal = calculateSolarEnergyTotal(resultArray, previousSolarEnergyTotal);
      //   let totalAmountSaved = calculateTotalAmountSaved(resultArray, previousTotalAmountSaved);
      //
      //   if (index === response.results.length - 1) {
      //     previousSolarEnergyTotal = solarEnergyTotal;
      //     previousTotalAmountSaved = totalAmountSaved;
      //   }
      //
      //   return {
      //     solarEnergyIndividual: calculateSolarEnergyIndividual(resultArray),
      //     solarEnergyTotal: solarEnergyTotal,
      //     internalBoughtEnergyPrice: calculateInternalBoughtEnergyPrice(resultArray),
      //     totalAmountSaved: totalAmountSaved,
      //   } as EfficiencyResult;
      // });

      const transformedResults = response.results.map(resultArray => ({
        solarEnergyIndividual: resultArray[0],
        solarEnergyTotal: resultArray[1],
        internalBoughtEnergyPrice: resultArray[2],
        totalAmountSaved: resultArray[3]
      }));

      function calculateSolarEnergyIndividual(data) {
        if (data.bitmap_plan_energy + data.bitmap_plan_no_energy === 0) {
          return 0;
        }
        return (data.bitmap_plan_energy / (data.bitmap_plan_energy + data.bitmap_plan_no_energy)) * 100;
      }

      function calculateSolarEnergyTotal(data, previousTotal = 0) {
        if (data.bitmap_plan_energy + data.bitmap_plan_no_energy === 0) {
          return previousTotal;
        }
        let currentPercentage = (data.bitmap_plan_energy / (data.bitmap_plan_energy + data.bitmap_plan_no_energy)) * 100;
        return previousTotal + currentPercentage;
      }

      function calculateInternalBoughtEnergyPrice(data) {
        return data.bitmap_plan_no_energy;
      }

      function calculateTotalAmountSaved(data, previousTotal = 0) {
        return previousTotal + data.bitmap_plan_energy;
      }

      efficiencyresultstore.set(transformedResults);

    } catch (err) {
      if (err.status !== 500) {
        return
      } else {
        console.error("Server error:", err);
      }
    }
  }

  // Initial call to start the data fetching process
  $: $isStarted && fetchData();
</script>

{#if $stepperData.households.length !== 0}
  <BaseLayout />
{:else}
  <Stepper />
{/if}
