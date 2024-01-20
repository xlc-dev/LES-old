<script lang="ts">
  import { stepperData, efficiencyresultstore, type EfficiencyResult, isStarted } from "./lib/stores";
  import { OpenAPI, SimulateService } from "./lib/client";

  import Stepper from "./components/stepper.svelte";
  import BaseLayout from "./components/baseLayout.svelte";

  OpenAPI.BASE = "http://localhost:8000";

  // const call = SimulateService.planApiSimulatePlanPost({
  //   chunkoffset: 0, // constantly increase with 7 when recursion occurs
  //   costmodel: $stepperData.costmodel,
  //   algorithm: $stepperData.algorithm,
  //   twinworld: $stepperData.twinworld,
  //   households: $stepperData.households,
  // }).then((res) => {
  //   // update other store(s) with results for dashboard
  //   // timedaily store (cumulative, not replacing)
  //
  //   // call the function again (recursion): chunkoffset + 7
  //
  // }).catch((err) => {
  //   // catch and show
  //   // if the error code is not 500, call the function again (recursion)
  // })
  //   // else load result component (can also be done in the if else statement below)

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

      const transformedResults = response.results.map((resultArray, index) => {
        let solarEnergyTotal = calculateSolarEnergyTotal(resultArray, previousSolarEnergyTotal);
        let totalAmountSaved = calculateTotalAmountSaved(resultArray, previousTotalAmountSaved);

        if (index === response.results.length - 1) {
          previousSolarEnergyTotal = solarEnergyTotal;
          previousTotalAmountSaved = totalAmountSaved;
        }

        return {
          solarEnergyIndividual: calculateSolarEnergyIndividual(resultArray),
          solarEnergyTotal: solarEnergyTotal,
          internalBoughtEnergyPrice: calculateInternalBoughtEnergyPrice(resultArray),
          totalAmountSaved: totalAmountSaved,
        } as EfficiencyResult;
      });

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

      efficiencyresultstore.update((store) => [...store, ...transformedResults]);

      // Check if more data needs to be fetched
      // if (/* condition to determine if more data is needed */) {
      //   fetchData(chunkoffset + 7); // Fetch next chunk
      // }
    } catch (err) {
      // Handle errors
      if (err.status !== 500) {
        // fetchData(chunkoffset + 7); // Attempt to fetch next chunk
        return
      } else {
        // Handle server error
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
