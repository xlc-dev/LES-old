<script lang="ts">
  /**
   * The household component contains the view that is displayed when an individual household
   * is clicked in the schedulable load table or in the simulation view. It contains additional
   * data about the selected household and its' appliances, which is regularly updated and
   * translated into a part of the visualisations in the dashboard component.
   */

  import { onDestroy, onMount } from "svelte";

  import { DatePicker } from "date-picker-svelte";

  import { endDate, startDate } from "../lib/stores";

  import type { HouseholdRead_Output } from "../lib/client";

  import SchedulableLoadGrid from "./schedulableLoadGrid.svelte";

  export let household: HouseholdRead_Output;
  let showDatePicker = false;
  let selectedDate = new Date($startDate * 1000);
  let weekDates = [];

  const hours = Array.from({ length: 24 }, (_, i) => i);

  /**
   * Toggles the visibility of the date picker.
   * @returns {void}
   */
  const toggleDatePicker = () => {
    showDatePicker = !showDatePicker;
  };

  /**
   * Handles the click event in an area outside the date picker.
   * @param {Event} event - The click event object.
   * @returns {void}
   */
  const handleClickOutsideDatePicker = (event) => {
    if (!event.target.closest(".date-picker-container")) {
      showDatePicker = false;
    }
  };

  /**
   * Contains logic that runs at initialisation, as soon as the component has been mounted.
   * In this component it initialises the event listener that checks whether an area outside a dropdown menu has been clicked.
   */
  onMount(() => {
    window.addEventListener("click", handleClickOutsideDatePicker);
    selectedDate = new Date($startDate * 1000);
  });

  /**
   * Contains logic that runs immediately before the component is unmounted.
   * In this component it destroys the event listener that checks whether an area outside a dropdown menu has been clicked.
   */
  onDestroy(() => {
    window.removeEventListener("click", handleClickOutsideDatePicker);
  });

  /**
   * Sets the minimum date for a given start date.
   * @param {number} startDate - The start date in seconds, which is a Unix timestamp.
   * @returns {Date} - The minimum date based on the start date.
   */
  $: setMinDate = new Date($startDate * 1000);

  /**
   * Sets the maximum date based on the provided end date timestamp.
   * @param {number} endDate - The end date in seconds, which is a Unix timestamp.
   * @returns {Date} - The maximum date based on the start date.
   */
  $: setMaxDate = new Date($endDate * 1000);

  /**
   * Generates an array of dates starting from the selected date up to a maximum of 6 days after.
   * @param {Date} selectedDate - The selected date.
   * @param {Date} setMaxDate - The maximum date allowed.
   * @returns {Array} - An array of dates starting from the selected date up to a maximum of 6 days after.
   */
  $: if (selectedDate) {
    weekDates = [selectedDate];

    let daysLeft = Math.min(
      6,
      Math.round((setMaxDate.getTime() - selectedDate.getTime()) / (24 * 60 * 60 * 1000))
    );

    for (let i = 1; i <= daysLeft; i++) {
      let nextDay = new Date(selectedDate);
      nextDay.setDate(nextDay.getDate() + i);
      weekDates.push(nextDay);
    }
  }
</script>

<div class="gap-4 pb-4 font-bold dark:text-les-white">
  <svg
    class="fill-dark h-24 dark:fill-white"
    version="1.1"
    id="Capa_1"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    viewBox="0 0 1000 345.804"
    xml:space="preserve">
    <g>
      <path
        d="M343.288,159.838L181.905,27.941c-5.242-4.283-12.77-4.283-18.009,0l-41.336,33.79V44.193c0-3.788-3.066-6.848-6.854-6.848
  H75.928c-3.788,0-6.854,3.063-6.854,6.848v61.251L2.516,159.838c-2.933,2.391-3.36,6.711-0.970,9.641
  c1.357,1.654,3.33,2.523,5.32,2.523c1.524,0,3.053-0.511,4.328-1.545l34.55-28.245v172.011c0,3.785,3.066,6.852,6.846,6.852
  h240.626c3.781,0,6.854-3.066,6.854-6.852V142.216l34.55,28.245c1.273,1.037,2.807,1.545,4.326,1.545
  c1.984,0,3.956-0.87,5.314-2.524C346.648,166.549,346.221,162.235,343.288,159.838z M82.779,51.041h26.071v21.888l-26.071,21.31
  V51.041z M286.367,307.369H59.44V131.015l107.596-87.939c3.414-2.791,8.316-2.791,11.731,0l107.6,87.939V307.369z" />
    </g>
    <text x="33%" y="70%" font-size="60" class="text-black dark:text-white"
      >{household.name} Data</text>
  </svg>
</div>

<div class="flex flex-col justify-between gap-12">
  <table class="min-w-full overflow-hidden rounded-lg leading-normal">
    <thead>
      <tr class="text-left text-xs uppercase tracking-wider">
        <th
          class="border-b-2 border-gray-200 bg-gray-100 px-5 py-3 text-gray-600 dark:bg-dark-table-header dark:text-les-white"
          >Name
        </th>

        <th
          class="border-b-2 border-gray-200 bg-gray-100 px-5 py-3 text-gray-600 dark:bg-dark-table-header dark:text-les-white"
          >Size
        </th>

        <th
          class="border-b-2 border-gray-200 bg-gray-100 px-5 py-3 text-gray-600 dark:bg-dark-table-header dark:text-les-white"
          >Energy Usage
        </th>

        <th
          class="border-b-2 border-gray-200 bg-gray-100 px-5 py-3 text-gray-600 dark:bg-dark-table-header dark:text-les-white"
          >Solar Panels
        </th>

        <th
          class="border-b-2 border-gray-200 bg-gray-100 px-5 py-3 text-gray-600 dark:bg-dark-table-header dark:text-les-white"
          >Solar Yield Yearly
        </th>
      </tr>
    </thead>

    <tbody>
      <tr class="text-left text-xs uppercase tracking-wider">
        <td
          class="border-b border-gray-200 bg-gray-100 px-5 py-6 text-gray-600 dark:bg-dark-table-header dark:text-les-white"
          >{household.name}</td>
        <td
          class="border-b border-gray-200 bg-gray-100 px-5 py-6 text-gray-600 dark:bg-dark-table-header dark:text-les-white"
          >{household.size}</td>
        <td
          class="border-b border-gray-200 bg-gray-100 px-5 py-6 text-gray-600 dark:bg-dark-table-header dark:text-les-white"
          >{household.energy_usage}</td>
        <td
          class="border-b border-gray-200 bg-gray-100 px-5 py-6 text-gray-600 dark:bg-dark-table-header dark:text-les-white"
          >{household.solar_panels}</td>
        <td
          class="border-b border-gray-200 bg-gray-100 px-5 py-6 text-gray-600 dark:bg-dark-table-header dark:text-les-white"
          >{household.solar_yield_yearly}</td>
      </tr>
    </tbody>
  </table>

  <table class="min-w-full overflow-hidden rounded-lg leading-normal">
    <thead>
      <tr class="text-left text-xs uppercase tracking-wider">
        <th
          class="border-b-2 border-gray-200 bg-gray-100 px-5 py-3 text-gray-600 dark:bg-dark-table-header dark:text-les-white"
          >Name
        </th>

        <th
          class="border-b-2 border-gray-200 bg-gray-100 px-5 py-3 text-gray-600 dark:bg-dark-table-header dark:text-les-white"
          >Power
        </th>

        <th
          class="border-b-2 border-gray-200 bg-gray-100 px-5 py-3 text-gray-600 dark:bg-dark-table-header dark:text-les-white"
          >Duration
        </th>

        <th
          class="border-b-2 border-gray-200 bg-gray-100 px-5 py-3 text-gray-600 dark:bg-dark-table-header dark:text-les-white"
          >Daily Usage
        </th>
      </tr>
    </thead>

    <tbody>
      {#each household.appliances as appliance}
        <tr class="text-left text-xs uppercase tracking-wider">
          <td
            class="border-b border-gray-200 bg-gray-100 px-5 py-6 text-gray-600 dark:bg-dark-table-header dark:text-les-white"
            >{appliance.name}</td>
          <td
            class="border-b border-gray-200 bg-gray-100 px-5 py-6 text-gray-600 dark:bg-dark-table-header dark:text-les-white"
            >{appliance.power}</td>
          <td
            class="border-b border-gray-200 bg-gray-100 px-5 py-6 text-gray-600 dark:bg-dark-table-header dark:text-les-white"
            >{appliance.duration}</td>
          <td
            class="border-b border-gray-200 bg-gray-100 px-5 py-6 text-gray-600 dark:bg-dark-table-header dark:text-les-white"
            >{appliance.daily_usage}</td>
        </tr>
      {/each}
    </tbody>
  </table>

  <hr class="my-2 border-black dark:border-les-white" />

  <h2 class="text-3xl font-bold dark:text-les-white">Schedulable Load</h2>

  <table class="min-w-full rounded-lg bg-white leading-normal dark:bg-dark-table-header">
    <div class="flex justify-center pt-4">
      <button class="date-picker-container relative" on:click|stopPropagation>
        <button
          class="rounded bg-les-blue px-4 py-2 text-white transition-colors duration-200 hover:brightness-110"
          on:click={toggleDatePicker}
          >Select Date
        </button>
        {#if showDatePicker}
          <div class="calendar absolute z-10 mt-2 rounded shadow-lg dark:calendar-dark">
            <DatePicker bind:value={selectedDate} min={setMinDate} max={setMaxDate} />
          </div>
        {/if}
      </button>
    </div>
    <tbody>
      <tr class="bg-white text-sm dark:bg-dark-table-header">
        <td colspan={3}>
          <div class="flex justify-center p-4">
            <div class="flex flex-col items-center gap-4">
              {#each weekDates.slice(0, 3) as date}
                <div class="mt-2 text-center text-gray-500">
                  {date.toLocaleDateString("en-US", { weekday: "long" })}
                </div>
                <SchedulableLoadGrid
                  appliances={household.appliances}
                  date={date.toLocaleDateString("en-US")}
                  dateNoFormat={date}
                  {hours} />
              {/each}
            </div>
          </div>
        </td>
        <td colspan={4}>
          <div class="flex justify-center p-4">
            <div class="flex flex-col items-center gap-4">
              {#each weekDates.slice(3, 7) as date}
                <div class="mt-2 text-center text-gray-500">
                  {date.toLocaleDateString("en-US", { weekday: "long" })}
                </div>
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
