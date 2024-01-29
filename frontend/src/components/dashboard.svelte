<script lang="ts">
  import { onDestroy } from "svelte";

  import { efficiencyresultstore, stepperData, runtime } from "../lib/stores";

  import Chart from "./chart.svelte";

  let sumEfficiencyIndividual: number = 0;
  let sumEfficiencyTotal: number = 0;
  let sumTotalMoneySaved: number = 0;

  // Listener function for individual efficiency updates
  const sumEfficiencyIndividualListener = efficiencyresultstore.subscribe(
    ($efficiencyresultstore) => {
      sumEfficiencyIndividual = $efficiencyresultstore.reduce(
        (accumulator, result) => accumulator + result.solarEnergyIndividual,
        0
      );
    }
  );

  // Listener function for total efficiency updates
  const sumEfficiencyTotalListener = efficiencyresultstore.subscribe(($efficiencyresultstore) => {
    sumEfficiencyTotal = $efficiencyresultstore.reduce(
      (accumulator, result) => accumulator + result.solarEnergyTotal,
      0
    );
  });

  // Listener function for total money saved updates
  const sumTotalMoneySavedListener = efficiencyresultstore.subscribe(($efficiencyresultstore) => {
    sumTotalMoneySaved = $efficiencyresultstore.reduce(
      (accumulator, result) => accumulator + result.totalAmountSaved,
      0
    );
  });

  // Destroy listeners on component destruction
  onDestroy(() => {
    sumEfficiencyIndividualListener();
    sumEfficiencyTotalListener();
    sumTotalMoneySavedListener();
  });

  // Computed property: Difference between total and individual efficiency
  $: sumEfficiencyNoSolar = sumEfficiencyTotal - sumEfficiencyIndividual;
</script>

<div class="max-w-7xl mx-auto">
  <Chart />
  <div
    class="mt-8 bg-white dark:bg-dark-table-row dark:text-white rounded-lg p-4 px-20 mb-8 shadow">
    <table class="w-full">
      <tr class="border-b border-gray-400">
        <td class="p-2">Number of Households:</td>
        <td class="p-2 min-w-40">{$stepperData.households.length}</td>
      </tr>
      {#if $stepperData.costmodel.fixed_price_ratio !== null}
        <tr class="border-b border-gray-400">
          <td class="p-2">Cost model fixed price ratio:</td>
          <td class="p-2 min-w-40">{$stepperData.costmodel.fixed_price_ratio}</td>
        </tr>
      {/if}
      {#if $stepperData.costmodel.price_network_buy_consumer !== null}
        <tr class="border-b border-gray-400">
          <td class="p-2">Cost model price network buy consumer:</td>
          <td class="p-2 min-w-40">{$stepperData.costmodel.price_network_buy_consumer}</td>
        </tr>
      {/if}
      {#if $stepperData.costmodel.price_network_sell_consumer !== null}
        <tr class="border-b border-gray-400">
          <td class="p-2">Cost model price network sell consumer:</td>
          <td class="p-2 min-w-40">{$stepperData.costmodel.price_network_sell_consumer}</td>
        </tr>
      {/if}
      {#if $stepperData.twinworld.energy_usage_factor !== null}
        <tr class="border-b border-gray-400">
          <td class="p-2">Twin world energy usage factor:</td>
          <td class="p-2 min-w-40">{$stepperData.twinworld.energy_usage_factor}</td>
        </tr>
      {/if}
      {#if $stepperData.twinworld.solar_panels_factor !== null}
        <tr class="border-b border-gray-400">
          <td class="p-2">Twin world solar panels factor:</td>
          <td class="p-2 min-w-40">{$stepperData.twinworld.solar_panels_factor}</td>
        </tr>
      {/if}
      {#if $stepperData.algorithm.max_temperature !== null}
        <tr class="border-b border-gray-400">
          <td class="p-2">Algorithm max temperature:</td>
          <td class="p-2 min-w-40">{$stepperData.algorithm.max_temperature}</td>
        </tr>
      {/if}
      {#if sumEfficiencyIndividual !== null}
        <tr class="border-b border-gray-400">
          <td class="p-2">Total saved by own solar panels:</td>
          <td class="p-2 min-w-40">{sumEfficiencyIndividual.toFixed(2)} kWh</td>
        </tr>
      {/if}
      {#if sumEfficiencyNoSolar !== null}
        <tr class="border-b border-gray-400">
          <td class="p-2">Total saved by other households' solar panels:</td>
          <td class="p-2 min-w-40">{sumEfficiencyNoSolar.toFixed(2)} kWh</td>
        </tr>
      {/if}
      {#if sumEfficiencyTotal !== null}
        <tr class="border-b border-gray-400">
          <td class="p-2">Total saved by the community:</td>
          <td class="p-2 min-w-40">{sumEfficiencyTotal.toFixed(2)} kWh</td>
        </tr>
      {/if}
      {#if sumTotalMoneySaved !== null}
        <tr class="border-b border-gray-400">
          <td class="p-2">Total money saved:</td>
          <td class="p-2 min-w-40">€{sumTotalMoneySaved.toFixed(2)}</td>
        </tr>
      {/if}
      {#if $runtime !== null}
        <tr>
          <td class="p-2">Runtime:</td>
          <td class="p-2 min-w-40">{$runtime} seconds</td>
        </tr>
      {/if}
    </table>
  </div>
</div>
