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

<div class="font-bold pb-4 gap-4 dark:text-les-white">
  <svg
    class="h-24 fill-dark dark:fill-white"
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
      {#if household.solar_panels}
        <g transform="translate(145, 75) scale(0.5)">
          <path fill="#fcdb33" d="M30,13.21A3.93,3.93,0,1,1,36.8,9.27L41.86,18A3.94,3.94,0,1,1,35.05,22L30,13.21Zm31.45,13A35.23,35.23,0,1,1,36.52,36.52,35.13,35.13,0,0,1,61.44,26.2ZM58.31,4A3.95,3.95,0,1,1,66.2,4V14.06a3.95,3.95,0,1,1-7.89,0V4ZM87.49,10.1A3.93,3.93,0,1,1,94.3,14l-5.06,8.76a3.93,3.93,0,1,1-6.81-3.92l5.06-8.75ZM109.67,30a3.93,3.93,0,1,1,3.94,6.81l-8.75,5.06a3.94,3.94,0,1,1-4-6.81L109.67,30Zm9.26,28.32a3.95,3.95,0,1,1,0,7.89H108.82a3.95,3.95,0,1,1,0-7.89Zm-6.15,29.18a3.93,3.93,0,1,1-3.91,6.81l-8.76-5.06A3.93,3.93,0,1,1,104,82.43l8.75,5.06ZM92.89,109.67a3.93,3.93,0,1,1-6.81,3.94L81,104.86a3.94,3.94,0,0,1,6.81-4l5.06,8.76Zm-28.32,9.26a3.95,3.95,0,1,1-7.89,0V108.82a3.95,3.95,0,1,1,7.89,0v10.11Zm-29.18-6.15a3.93,3.93,0,0,1-6.81-3.91l5.06-8.76A3.93,3.93,0,1,1,40.45,104l-5.06,8.75ZM13.21,92.89a3.93,3.93,0,1,1-3.94-6.81L18,81A3.94,3.94,0,1,1,22,87.83l-8.76,5.06ZM4,64.57a3.95,3.95,0,1,1,0-7.89H14.06a3.95,3.95,0,1,1,0,7.89ZM10.1,35.39A3.93,3.93,0,1,1,14,28.58l8.76,5.06a3.93,3.93,0,1,1-3.92,6.81L10.1,35.39Z"/>
        </g>
      {/if}
    </g>
    <text x="175" y="200" font-size="30" text-anchor="middle" class="dark:text-white text-black">{household.size}m²</text>
    <text x="175" y="275" font-size="30" text-anchor="middle" class="dark:text-white text-black">{household.name}</text>
  </svg>
</div>

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

  <hr class="my-2 border-black dark:border-les-white" />

  <h2 class="font-bold text-3xl dark:text-les-white">Schedulable Load</h2>

  <table class="bg-white dark:bg-dark-table-header min-w-full leading-normal rounded-lg">
    <div class="flex justify-center pt-4">
      <button class="date-picker-container relative" on:click|stopPropagation>
        <button
          class="px-4 py-2 bg-les-blue text-white rounded hover:brightness-110 transition-colors duration-200"
          on:click={toggleDatePicker}
          >Select Date
        </button>
        {#if showDatePicker}
          <div class="absolute z-10 mt-2 rounded shadow-lg calendar dark:calendar-dark">
            <DatePicker bind:value={selectedDate} min={setMinDate} max={setMaxDate} />
          </div>
        {/if}
      </button>
    </div>
    <tbody>
      <tr class="bg-white text-sm dark:bg-dark-table-header">
        <td colspan={3}>
          <div class="p-4 flex justify-center">
            <div class="flex flex-col items-center gap-4">
              {#each weekDates.slice(0, 3) as date}
                <div class="text-center mt-2 text-gray-500">
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
          <div class="p-4 flex justify-center">
            <div class="flex flex-col items-center gap-4">
              {#each weekDates.slice(3, 7) as date}
                <div class="text-center mt-2 text-gray-500">
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
