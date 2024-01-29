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
  import { activatedHousehold, endDate, startDate } from "../lib/stores";
  import { onDestroy, onMount } from "svelte";

  export let household: HouseholdRead_Output;
  let showDatePicker = false;
  let selectedDate = new Date();
  let weekDates = [];
  let formattedDate: string;

  $: setMinDate = new Date($startDate * 1000);
  $: setMaxDate = new Date($endDate * 1000);
  $: if (selectedDate) {
    weekDates = [new Date(selectedDate)];
    for (let i = 1; i <= 6; i++) {
      let nextDay = new Date(selectedDate);
      nextDay.setDate(nextDay.getDate() + i);
      weekDates.push(nextDay);
    }
  }

  const hours = Array.from({ length: 24 }, (_, i) => i);

  const toggleDatePicker = () => {
    showDatePicker = !showDatePicker;
  };

  const handleClickOutside = (event) => {
    if (!event.target.closest(".date-picker-container")) {
      showDatePicker = false;
    }
  };

  onMount(() => {
    window.addEventListener("click", handleClickOutside);
  });

  onDestroy(() => {
    window.removeEventListener("click", handleClickOutside);
  });

  $: if (selectedDate) {
    formattedDate = new Date(selectedDate).toLocaleDateString("en-US");
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
  <button class="date-picker-container relative" on:click|stopPropagation>
    <button
      class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      on:click={toggleDatePicker}
      >Select Date
    </button>
    {#if showDatePicker}
      <div
        class="date-picker-popup absolute z-10 mt-2 bg-white border border-gray-300 rounded shadow-lg p-4">
        <DatePicker bind:value={selectedDate} min={setMinDate} max={setMaxDate} />
      </div>
    {/if}
  </button>
  {#if formattedDate}
    <div class="text-center mt-2">
      <span class="text-lg font-medium text-les-white">Selected date: {formattedDate}</span>
    </div>
  {/if}
  <table>
    <tbody>
      <tr
        class="bg-white hover:bg-white text-sm dark:bg-dark-table-row border-b border-gray-200 dark:border-les-white">
        <td colspan={7}>
          <div class="p-4 flex justify-center">
            <div class="flex flex-col items-center gap-4">
              {#each weekDates as date}
                <SchedulableLoadGrid
                  appliances={household.appliances}
                  date={date.toLocaleDateString("en-US")}
                  dateNoFormat={date}
                  {hours} />
              {/each}
            </div>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
</div>

<hr class="my-8 border-black dark:border-les-white" />
