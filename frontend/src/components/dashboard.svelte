<script lang="ts">
  /**
   * The dashboard component contains the dashboard view in which the results of the simulation are displayed.
   * It also contains the chart component that displays the results in a chart.
   */

  import { onDestroy } from "svelte";

  import { efficiencyresultstore, stepperData, runtime } from "../lib/stores";

  import Chart from "./chart.svelte";

  let sumEfficiencyIndividual: number = 0;
  let sumEfficiencyTotal: number = 0;
  let sumTotalMoneySaved: number = 0;

  /**
   * Subscribes to the efficiency result store and checks for individual efficiency updates.
   * @param {function} $efficiencyresultstore - The callback function that is invoked when individual efficiency updates have been detected.
   * @returns {object} - A reference to the subscription.
   */
  const sumEfficiencyIndividualListener = efficiencyresultstore.subscribe(
    ($efficiencyresultstore) => {
      sumEfficiencyIndividual = $efficiencyresultstore.reduce(
        (accumulator, result) => accumulator + result.solarEnergyIndividual,
        0
      );
    }
  );

  /**
   * Subscribes to the efficiency result store and checks for total efficiency updates.
   * @param {function} $efficiencyresultstore - The callback function that is invoked when individual efficiency updates have been detected.
   */
  const sumEfficiencyTotalListener = efficiencyresultstore.subscribe(($efficiencyresultstore) => {
    sumEfficiencyTotal = $efficiencyresultstore.reduce(
      (accumulator, result) => accumulator + result.solarEnergyTotal,
      0
    );
  });

  /**
   * Subscribes to the efficiency result store and checks for updates on the total money saved.
   * @param {function} $efficiencyresultstore - The callback function that is invoked when individual efficiency updates have been detected.
   */
  const sumTotalMoneySavedListener = efficiencyresultstore.subscribe(($efficiencyresultstore) => {
    sumTotalMoneySaved = $efficiencyresultstore.reduce(
      (accumulator, result) => accumulator + result.totalAmountSaved,
      0
    );
  });

  /*
   * Contains logic that runs immediately before the component is unmounted.
   * In this component it destroys the listener functions.
   */
  onDestroy(() => {
    sumEfficiencyIndividualListener();
    sumEfficiencyTotalListener();
    sumTotalMoneySavedListener();
  });

  /**
   * Calculates the difference between the total and individual efficiency
   *
   * @param {number} sumEfficiencyTotal - The value of the total efficiency.
   * @param {number} sumEfficiencyIndividual - The value of the individual efficiency.
   * @returns {number} - The difference between the two efficiency values.
   */
  $: sumEfficiencyNoSolar = sumEfficiencyTotal - sumEfficiencyIndividual;
</script>

<div class="mx-auto max-w-7xl">
  <Chart />
  <div class="mt-8 bg-white dark:bg-les-gray-600 dark:text-white rounded-lg p-4 px-20 mb-8 shadow">
    <table class="w-full">
      <tr class="border-b border-gray-400">
        <td class="p-2">Number of Households:</td>
        <td class="min-w-40 p-2">{$stepperData.households.length}</td>
      </tr>
      {#if sumEfficiencyIndividual !== null}
        <tr class="border-b border-gray-400">
          <td class="p-2">Total saved by own solar panels:</td>
          <td class="min-w-40 p-2">{sumEfficiencyIndividual.toFixed(2)} kWh</td>
        </tr>
      {/if}
      {#if sumEfficiencyNoSolar !== null}
        <tr class="border-b border-gray-400">
          <td class="p-2">Total saved by other households' solar panels:</td>
          <td class="min-w-40 p-2">{sumEfficiencyNoSolar.toFixed(2)} kWh</td>
        </tr>
      {/if}
      {#if sumEfficiencyTotal !== null}
        <tr class="border-b border-gray-400">
          <td class="p-2">Total saved by the community:</td>
          <td class="min-w-40 p-2">{sumEfficiencyTotal.toFixed(2)} kWh</td>
        </tr>
      {/if}
      {#if sumTotalMoneySaved !== null}
        <tr class="border-b border-gray-400">
          <td class="p-2">Total money saved:</td>
          <td class="min-w-40 p-2">€{sumTotalMoneySaved.toFixed(2)}</td>
        </tr>
      {/if}
      {#if $runtime !== null}
        <tr>
          <td class="p-2">Runtime:</td>
          <td class="min-w-40 p-2">{$runtime} seconds</td>
        </tr>
      {/if}
    </table>
  </div>
</div>
