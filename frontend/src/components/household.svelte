<script lang="ts">
  /*
  The household component contains the view that is displayed when an individual household
  is clicked in the schedulable load table or in the simulation view. It contains additional
  data about the selected household and its' appliances, which is regularly updated and
  translated into a part of the visualisations in the dashboard component.
  */
  import type { HouseholdRead_Output } from "../lib/client";
  import SchedulableLoadGrid from "./schedulableLoadGrid.svelte";
  import { DatePicker } from "date-picker-svelte";

  export let household: HouseholdRead_Output;
  let selectedDate = new Date();
  let currentDate = new Date();

  // Checks if the selected date is in the past
  const isPastDate = (date) => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return date < today;
  };

  // Fetches data for the selected date
  // This function needs to be supplemented with logic that fetches the required data
  const fetchDataForDate = async (date) => {};

  // Updates the displayed data when a new data has been selected
  $: if (isPastDate(selectedDate)) {
    fetchDataForDate(selectedDate);
  }
</script>

<h1 class="font-bold text-4xl pb-4 flex items-center gap-4 dark:text-les-white">
  <img src="/house.svg" alt="" class="h-24" />{household.name} Data
</h1>

<div class="flex flex-col gap-12 justify-between">
  <table class="min-w-full leading-normal rounded-lg overflow-hidden">
    <thead>
      <tr class="text-xs text-left uppercase tracking-wider">
        <th
          class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-gray-600 dark:text-les-white dark:bg-dark-table-header"
          >Name
        </th>

        <th
          class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-gray-600 dark:text-les-white dark:bg-dark-table-header"
          >Size
        </th>

        <th
          class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-gray-600 dark:text-les-white dark:bg-dark-table-header"
          >Energy Usage
        </th>

        <th
          class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-gray-600 dark:text-les-white dark:bg-dark-table-header"
          >Solar Panels
        </th>

        <th
          class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-gray-600 dark:text-les-white dark:bg-dark-table-header"
          >Solar Yield Yearly
        </th>
      </tr>
    </thead>

    <tbody>
      <tr class="text-xs text-left uppercase tracking-wider">
        <td
          class="px-5 py-6 border-b border-gray-200 bg-gray-100 text-gray-600 dark:text-les-white dark:bg-dark-table-header"
          >{household.name}</td>
        <td
          class="px-5 py-6 border-b border-gray-200 bg-gray-100 text-gray-600 dark:text-les-white dark:bg-dark-table-header"
          >{household.size}</td>
        <td
          class="px-5 py-6 border-b border-gray-200 bg-gray-100 text-gray-600 dark:text-les-white dark:bg-dark-table-header"
          >{household.energy_usage}</td>
        <td
          class="px-5 py-6 border-b border-gray-200 bg-gray-100 text-gray-600 dark:text-les-white dark:bg-dark-table-header"
          >{household.solar_panels}</td>
        <td
          class="px-5 py-6 border-b border-gray-200 bg-gray-100 text-gray-600 dark:text-les-white dark:bg-dark-table-header"
          >{household.solar_yield_yearly}</td>
      </tr>
    </tbody>
  </table>

  <table class="min-w-full leading-normal rounded-lg overflow-hidden">
    <thead>
      <tr class="text-xs text-left uppercase tracking-wider">
        <th
          class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-gray-600 dark:text-les-white dark:bg-dark-table-header"
          >Name
        </th>

        <th
          class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-gray-600 dark:text-les-white dark:bg-dark-table-header"
          >Power
        </th>

        <th
          class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-gray-600 dark:text-les-white dark:bg-dark-table-header"
          >Duration
        </th>

        <th
          class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-gray-600 dark:text-les-white dark:bg-dark-table-header"
          >Daily Usage
        </th>
      </tr>
    </thead>

    <tbody>
      {#each household.appliances as appliance}
        <tr class="text-xs text-left uppercase tracking-wider">
          <td
            class="px-5 py-6 border-b border-gray-200 bg-gray-100 text-gray-600 dark:text-les-white dark:bg-dark-table-header"
            >{appliance.name}</td>
          <td
            class="px-5 py-6 border-b border-gray-200 bg-gray-100 text-gray-600 dark:text-les-white dark:bg-dark-table-header"
            >{appliance.power}</td>
          <td
            class="px-5 py-6 border-b border-gray-200 bg-gray-100 text-gray-600 dark:text-les-white dark:bg-dark-table-header"
            >{appliance.duration}</td>
          <td
            class="px-5 py-6 border-b border-gray-200 bg-gray-100 text-gray-600 dark:text-les-white dark:bg-dark-table-header"
            >{appliance.daily_usage}</td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>

<hr class="my-8 border-black dark:border-les-white" />
