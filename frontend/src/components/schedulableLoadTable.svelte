<script lang="ts">
  /**
   * The schedulableLoadTable component contians the table of the schedulable load view that
   * consists of the table and cards of the households that are included in the selected or
   * created twin world of the current session and filters that can be used to only display
   * specific items of the table. Each card in the table contains data about its' corresponding
   * household and can be expanded to view its' schedulable load grid raster.
   */

  import { onDestroy, onMount } from "svelte";
  import { slide } from "svelte/transition";

  import { DatePicker } from "date-picker-svelte";

  import { activatedHousehold, stepperData, startDate, endDate } from "../lib/stores";

  import SchedulableLoadGrid from "./schedulableLoadGrid.svelte";
  import SortIcon from "./sortIcon.svelte";

  let filters = {
    size: Array.from({ length: 10 }, (_, i) => i + 1),
    energyUsage: Array.from({ length: 10 }, (_, i) => ({ min: i * 1000, max: (i + 1) * 1000 })),
    solarPanels: Array.from({ length: 21 }, (_, i) => i),
    solarYieldYearly: Array.from({ length: 10 }, (_, i) => ({
      min: i * 1000,
      max: (i + 1) * 1000,
    })),
    appliances: ["Dishwasher", "Washing Machine", "Tumble Dryer", "Stove", "Electric Vehicle"],
  };

  let selectedFilters = {
    size: [],
    energyUsage: [],
    solarPanels: [],
    solarYieldYearly: [],
    appliances: [],
  };

  let expandedRow = null;
  let sortColumn = null;
  let sortOrder = "asc";
  let searchQuery = "";
  let showDropdown = null;
  let filteredData = [];
  let showDatePicker = false;
  let selectedDate = new Date();
  let showLegend = false;
  let formattedDate: string;

  const hours = Array.from({ length: 24 }, (_, i) => i);

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
   * Displays a dropdown menu of a filter when its corresponding button is clicked.
   * @param {string} filterName - The name of the filter.
   * @returns {void}
   */
  const toggleDropdown = (filterName: string) => {
    showDropdown = showDropdown === filterName ? null : filterName;
  };

  /**
   * Toggles the visibility of the date picker.
   * @returns {void}
   */
  const toggleDatePicker = () => {
    showDatePicker = !showDatePicker;
  };

  /**
   * Toggles the visibility of the legend card.
   * @returns {void}
   */
  const toggleCard = () => {
    showLegend = !showLegend;
  };

  /**
   * Retracts the displayed dropdown menu when an area outside the dropdown menu has been clicked.
   * @param filterName
   * @returns {void}
   */
  const handleClickOutsideFilter = (filterName: string) => {
    return (event: any) => {
      if (!event.target.closest(`#${filterName}-dropdown`)) {
        showDropdown = null;
      }
    };
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

    if (!event.target.closest(".legend")) {
      showLegend = false;
    }
  };

  /**
   * Modifies the name of a filter so that it's written in camel case.
   * @param {string} camelCase - The string to be converted.
   * @returns {string} - The converted readable name.
   */
  const toReadableName = (camelCase: string) => {
    return camelCase.replace(/([A-Z])/g, " $1").replace(/^./, (str) => str.toUpperCase());
  };

  /**
   * Expands a card of a household in the schedulable load table when its row has been clicked.
   * @param {number} id - The id of the card to be expanded.
   */
  const toggleRow = (id: number) => {
    expandedRow = expandedRow === id ? null : id;
  };

  /**
   * Sorts certain columns of the schedulable load table by ascending or descending based on how often a sort button has been clicked.
   * @param {string} column - The column to sort the data by.
   * @returns {void}
   */
  const sortData = (column: string) => {
    if (sortColumn === column) {
      sortOrder = sortOrder === "asc" ? "desc" : "asc";
    } else {
      sortColumn = column;
      sortOrder = "desc";
    }
    sortColumn = column;
    filteredData = filteredData.slice().sort((a, b) => {
      if (a[column] < b[column]) return sortOrder === "asc" ? -1 : 1;
      if (a[column] > b[column]) return sortOrder === "asc" ? 1 : -1;
      return 0;
    });
  };

  /**
   * Contains logic that runs at initialisation, as soon as the component has been mounted.
   * In this component it initialises the event listener that handles button clicks of filters in the schedulable load table.
   */
  onMount(() => {
    window.addEventListener("click", handleClickOutsideDatePicker);
    document.addEventListener("click", (event: any) => {
      for (const filterName in filters) {
        const filterDropdown = document.getElementById(`${filterName}-dropdown`);
        if (filterDropdown && !filterDropdown.contains(event.target)) {
          showDropdown = null;
        }
      }
    });
    if (setMinDate) {
      selectedDate = setMinDate;
    }
  });

  /**
   * Contains logic that runs immediately before the component is unmounted.
   * In this component it destroys the event listener that handles button clicks of filters in the schedulable load table.
   */
  onDestroy(() => {
    window.removeEventListener("click", handleClickOutsideDatePicker);
  });

  /**
   * Applies the filter logic on the schedulable load table.
   * @param {string} searchQuery - The search query to filter by. If empty, all items will be returned.
   * @param {Object} selectedFilters - The selected filters to apply.
   * @param {Array} selectedFilters.size - The selected size filters. If empty, all sizes will be considered a match.
   * @param {Array} selectedFilters.energyUsage - The selected energy usage filters. If empty, all energy usages will be considered a match.
   * @param {Array} selectedFilters.solarPanels - The selected solar panels filters. If empty, all solar panels will be considered a match.
   * @param {Array} selectedFilters.solarYieldYearly - The selected solar yield yearly filters. If empty, all solar yield yearly values will be considered a match.
   * @param {Array} selectedFilters.appliances - The selected appliances filters. If empty, all appliances will be considered a match.
   * @return {Array} The filtered stepper data based on the search query and selected filters.
   */
  $: {
    filteredData = $stepperData.households.filter((item) => {
      const matchesSearch =
        !searchQuery ||
        item.id.toString().includes(searchQuery) ||
        item.name.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesSize =
        selectedFilters.size.length === 0 || selectedFilters.size.includes(item.size);
      const matchesEnergyUsage =
        selectedFilters.energyUsage.length === 0 ||
        selectedFilters.energyUsage.some(
          (range) => item.energy_usage >= range.min && item.energy_usage < range.max
        );
      const matchesSolarPanels =
        selectedFilters.solarPanels.length === 0 ||
        selectedFilters.solarPanels.includes(item.solar_panels);
      const matchesSolarYieldYearly =
        selectedFilters.solarYieldYearly.length === 0 ||
        selectedFilters.solarYieldYearly.some(
          (range) => item.solar_yield_yearly >= range.min && item.solar_yield_yearly < range.max
        );
      const matchesAppliances =
        selectedFilters.appliances.length === 0 ||
        item.appliances.some((appliance) => selectedFilters.appliances.includes(appliance.name));

      return (
        matchesSearch &&
        matchesSize &&
        matchesEnergyUsage &&
        matchesSolarPanels &&
        matchesSolarYieldYearly &&
        matchesAppliances
      );
    });
  }

  /**
   * Updates the selected date when a date has been selected in the date picker.
   * @param {string} selectedDate - The selected date in a string format.
   * @return {string} - The formatted date string.
   */
  $: if (selectedDate) {
    formattedDate = new Date(selectedDate).toLocaleDateString("en-US");
  }
</script>

<div
  class="mb-4 flex items-center justify-between rounded-lg bg-gray-100 p-2 dark:bg-les-gray-700">
  <div class="flex space-x-4">
    <input
      type="text"
      class="rounded-md border border-gray-300 px-3 py-2 dark:bg-les-gray-600 dark:text-les-white"
      placeholder="Search by ID or NAME"
      bind:value={searchQuery} />

    {#each Object.entries(filters) as [filterName, options]}
      <button
        class="relative"
        id={`${filterName}-dropdown`}
        on:click|stopPropagation={handleClickOutsideFilter(filterName)}>
        <button
          class="rounded-md border border-gray-300 bg-white px-3 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 dark:bg-les-gray-600 dark:text-les-white"
          on:click={() => toggleDropdown(filterName)}
          on:keydown={(e) => e.key === "Enter" && toggleDropdown(filterName)}>
          {toReadableName(filterName)}
        </button>

        {#if showDropdown === filterName}
          <div
            class="absolute left-0 z-10 mt-2 w-56 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 dark:bg-les-gray-600"
            in:slide={{ duration: 500 }}
            out:slide={{ duration: 500 }}>
            <div class="py-1">
              {#each options as option}
                <label
                  class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-les-white hover:dark:bg-les-gray-700">
                  <input
                    type="checkbox"
                    class="mr-2"
                    bind:group={selectedFilters[filterName]}
                    value={option}
                    on:change={() => {}} />
                  {typeof option === "object" ? `${option.min}-${option.max}` : option}
                </label>
              {/each}
            </div>
          </div>
        {/if}
      </button>
    {/each}
    <button
      class="ml-2 rounded bg-les-gray-500 px-4 py-2 text-white hover:brightness-110"
      on:click|stopPropagation={toggleCard}>Legend</button>
    <button class="date-picker-container relative" on:click|stopPropagation>
      <button
        class="rounded bg-les-blue px-4 py-2 text-white transition-colors duration-200 hover:brightness-110"
        on:click={toggleDatePicker}>Select Date</button>
      {#if showDatePicker}
        <div class="calendar absolute z-10 mt-2 rounded dark:calendar-dark">
          <DatePicker bind:value={selectedDate} min={setMinDate} max={setMaxDate} />
        </div>
      {/if}
    </button>
  </div>

  {#if showLegend}
    <div class="fixed inset-0 flex items-center justify-center">
      <button
        on:click={toggleCard}
        class="w-100 legend relative z-10 rounded border border-gray-300 bg-white p-4 shadow-lg dark:bg-sidebar dark:text-les-white">
        <button
          class="absolute right-2 top-2 p-2 text-xl text-gray-600 hover:text-gray-800"
          on:click={toggleCard}>
          <svg
            class="h-4 w-4 fill-current text-black transition-colors duration-200 hover:text-les-highlight dark:text-les-white"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24">
            <path
              d="M12 10.586l4.95-4.95a1 1 0 111.414 1.414L13.414 12l4.95 4.95a1 1 0 11-1.414 1.414L12 13.414l-4.95 4.95a1 1 0 11-1.414-1.414L10.586 12 5.636 7.05a1 1 0 111.414-1.414L12 10.586z" />
          </svg>
        </button>
        <div class="mb-2 flex items-center">
          <div class="mr-2 h-4 w-4 bg-gray-700"></div>
          <p>contain the time slots that are unavailable to plan appliances in.</p>
        </div>
        <div class="mb-2 flex items-center">
          <div class="mr-2 h-4 w-4 bg-les-blue"></div>
          <p>contain the time slots that are available to plan appliances in.</p>
        </div>
        <div class="mb-2 flex items-center">
          <div class="mr-2 h-4 w-4 bg-green-700"></div>
          <p>indicate that the planned energy used is drawn from solar panels.</p>
        </div>
        <div class="flex items-center">
          <div class="mr-2 h-4 w-4 bg-les-red"></div>
          <p>indicate that the planned energy used is drawn from the national grid.</p>
        </div>
      </button>
    </div>
  {/if}
</div>

<table class="min-w-full overflow-hidden rounded-lg leading-normal">
  <thead>
    <tr>
      <th
        class="border-b-2 border-gray-200 bg-gray-100 px-5 py-3 text-left text-xs uppercase tracking-wider text-gray-600 dark:bg-les-gray-700 dark:text-les-white">
        ID
        <SortIcon
          isSortedAsc={sortColumn === "id" && sortOrder === "asc"}
          isSortedDesc={sortColumn === "id" && sortOrder === "desc"}
          onSort={() => sortData("id")} />
      </th>

      <th
        class="border-b-2 border-gray-200 bg-gray-100 px-5 py-3 text-left text-xs uppercase tracking-wider text-gray-600 dark:bg-les-gray-700 dark:text-les-white">
        Name
        <SortIcon
          isSortedAsc={sortColumn === "name" && sortOrder === "asc"}
          isSortedDesc={sortColumn === "name" && sortOrder === "desc"}
          onSort={() => sortData("name")} />
      </th>

      <th
        class="border-b-2 border-gray-200 bg-gray-100 px-5 py-3 text-left text-xs uppercase tracking-wider text-gray-600 dark:bg-les-gray-700 dark:text-les-white">
        Size
        <SortIcon
          isSortedAsc={sortColumn === "size" && sortOrder === "asc"}
          isSortedDesc={sortColumn === "size" && sortOrder === "desc"}
          onSort={() => sortData("size")} />
      </th>

      <th
        class="border-b-2 border-gray-200 bg-gray-100 px-5 py-3 text-left text-xs uppercase tracking-wider text-gray-600 dark:bg-les-gray-700 dark:text-les-white">
        Energy Usage
        <SortIcon
          isSortedAsc={sortColumn === "energy_usage" && sortOrder === "asc"}
          isSortedDesc={sortColumn === "energy_usage" && sortOrder === "desc"}
          onSort={() => sortData("energy_usage")} />
      </th>

      <th
        class="border-b-2 border-gray-200 bg-gray-100 px-5 py-3 text-left text-xs uppercase tracking-wider text-gray-600 dark:bg-les-gray-700 dark:text-les-white">
        Solar Panels
        <SortIcon
          isSortedAsc={sortColumn === "solar_panels" && sortOrder === "asc"}
          isSortedDesc={sortColumn === "solar_panels" && sortOrder === "desc"}
          onSort={() => sortData("solar_panels")} />
      </th>

      <th
        class="border-b-2 border-gray-200 bg-gray-100 px-5 py-3 text-left text-xs uppercase tracking-wider text-gray-600 dark:bg-les-gray-700 dark:text-les-white">
        Solar Yield Yearly
        <SortIcon
          isSortedAsc={sortColumn === "solar_yield_yearly" && sortOrder === "asc"}
          isSortedDesc={sortColumn === "solar_yield_yearly" && sortOrder === "desc"}
          onSort={() => sortData("solar_yield_yearly")} />
      </th>

      <th
        class="border-b-2 border-gray-200 bg-gray-100 px-5 py-3 text-left text-xs uppercase tracking-wider text-gray-600 dark:bg-les-gray-700 dark:text-les-white">
        Appliances
      </th>
    </tr>
  </thead>

  <tbody>
    {#each filteredData as data}
      <tr
        class="cursor-pointer bg-white text-sm hover:!bg-gray-100 dark:bg-les-gray-600 dark:text-white hover:dark:!bg-les-gray-700"
        on:click={() => toggleRow(data.id)}>
        <td class="px-5 py-5">
          <button
            class="flex cursor-pointer items-center gap-4 text-gray-800 transition-colors duration-200 hover:!text-les-blue dark:text-les-white"
            on:click={() => ($activatedHousehold = data)}>
            {data.id}
          </button>
        </td>

        <td class="px-5 py-5">
          <button
            class="flex cursor-pointer items-center gap-4 text-gray-800 transition-colors duration-200 hover:!text-les-blue dark:text-les-white"
            on:click={() => ($activatedHousehold = data)}>
            {data.name}
          </button>
        </td>

        <td class="px-5 py-5">
          {data.size}
        </td>

        <td class="px-5 py-5">
          {data.energy_usage}
        </td>

        <td class="px-5 py-5">
          {data.solar_panels}
        </td>

        <td class="px-5 py-5">
          {data.solar_yield_yearly}
        </td>

        <td class={expandedRow === data.id ? "px-5 py-5" : "px-5 py-5"}>
          {#each data.appliances as appliance}
            {appliance.name}
            <br />
          {/each}
        </td>
      </tr>
      {#if expandedRow === data.id}
        <tr
          class="border-b border-gray-200 bg-white text-sm hover:bg-white dark:border-les-white dark:bg-les-gray-600">
          <td colspan={7}>
            <div transition:slide class="flex justify-center p-4">
              {#key formattedDate}
                <SchedulableLoadGrid
                  appliances={data.appliances}
                  date={formattedDate}
                  dateNoFormat={selectedDate}
                  {hours} />
              {/key}
            </div>
          </td>
        </tr>
      {/if}
    {/each}
  </tbody>
</table>
