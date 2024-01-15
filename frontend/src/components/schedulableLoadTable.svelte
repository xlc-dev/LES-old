<script lang="ts">
  import { onMount } from "svelte";
  import { get } from "svelte/store";
  import { slide } from "svelte/transition";

  import { activatedHousehold, stepperData } from "../lib/stores";

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

  const hours = Array.from({ length: 24 }, (_, i) => i);

  const toggleDropdown = (filterName: string) => {
    showDropdown = showDropdown === filterName ? null : filterName;
  };

  const createHandleClickOutside = (filterName: string) => {
    return (event: any) => {
      if (!event.target.closest(`#${filterName}-dropdown`)) {
        showDropdown = null;
      }
    };
  };

  const toReadableName = (camelCase: string) => {
    return camelCase.replace(/([A-Z])/g, " $1").replace(/^./, (str) => str.toUpperCase());
  };

  const toggleRow = (id: number) => {
    expandedRow = expandedRow === id ? null : id;
  };

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

  onMount(() => {
    document.addEventListener("click", (event: any) => {
      for (const filterName in filters) {
        const filterDropdown = document.getElementById(`${filterName}-dropdown`);
        if (filterDropdown && !filterDropdown.contains(event.target)) {
          showDropdown = null;
        }
      }
    });
  });

  $: {
    let data = get(stepperData);
    filteredData = data.filter((item) => {
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
</script>

<div
  class="flex justify-between items-center rounded-lg bg-gray-100 p-2 dark:bg-dark-table-header mb-4">
  <div class="flex space-x-4">
    <input
      type="text"
      class="px-3 py-2 border border-gray-300 rounded-md dark:bg-dark-table-row dark:text-les-white"
      placeholder="Search by ID or NAME"
      bind:value={searchQuery} />

    {#each Object.entries(filters) as [filterName, options]}
      <button
        class="relative"
        id={`${filterName}-dropdown`}
        on:click|stopPropagation={createHandleClickOutside(filterName)}>
        <button
          class="px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 dark:bg-dark-table-row dark:text-les-white"
          on:click={() => toggleDropdown(filterName)}
          on:keydown={(e) => e.key === "Enter" && toggleDropdown(filterName)}>
          {toReadableName(filterName)}
        </button>

        {#if showDropdown === filterName}
          <div
            class="absolute left-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-10 dark:bg-dark-table-row"
            in:slide={{ duration: 500 }}
            out:slide={{ duration: 500 }}>
            <div class="py-1">
              {#each options as option}
                <label
                  class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-les-white hover:dark:bg-dark-table-header">
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
  </div>
</div>

<table class="min-w-full leading-normal rounded-lg overflow-hidden">
  <thead>
    <tr>
      <th
        class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs text-gray-600 dark:text-les-white uppercase tracking-wider dark:bg-dark-table-header">
        ID
        <SortIcon
          isSortedAsc={sortColumn === "id" && sortOrder === "asc"}
          isSortedDesc={sortColumn === "id" && sortOrder === "desc"}
          onSort={() => sortData("id")} />
      </th>

      <th
        class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs text-gray-600 dark:text-les-white uppercase tracking-wider dark:bg-dark-table-header">
        Name
        <SortIcon
          isSortedAsc={sortColumn === "name" && sortOrder === "asc"}
          isSortedDesc={sortColumn === "name" && sortOrder === "desc"}
          onSort={() => sortData("name")} />
      </th>

      <th
        class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs text-gray-600 dark:text-les-white uppercase tracking-wider dark:bg-dark-table-header">
        Size
        <SortIcon
          isSortedAsc={sortColumn === "size" && sortOrder === "asc"}
          isSortedDesc={sortColumn === "size" && sortOrder === "desc"}
          onSort={() => sortData("size")} />
      </th>

      <th
        class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs text-gray-600 dark:text-les-white uppercase tracking-wider dark:bg-dark-table-header">
        Energy Usage
        <SortIcon
          isSortedAsc={sortColumn === "energy_usage" && sortOrder === "asc"}
          isSortedDesc={sortColumn === "energy_usage" && sortOrder === "desc"}
          onSort={() => sortData("energy_usage")} />
      </th>

      <th
        class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs text-gray-600 dark:text-les-white uppercase tracking-wider dark:bg-dark-table-header">
        Solar Panels
        <SortIcon
          isSortedAsc={sortColumn === "solar_panels" && sortOrder === "asc"}
          isSortedDesc={sortColumn === "solar_panels" && sortOrder === "desc"}
          onSort={() => sortData("solar_panels")} />
      </th>

      <th
        class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs text-gray-600 dark:text-les-white uppercase tracking-wider dark:bg-dark-table-header">
        Solar Yield Yearly
        <SortIcon
          isSortedAsc={sortColumn === "solar_yield_yearly" && sortOrder === "asc"}
          isSortedDesc={sortColumn === "solar_yield_yearly" && sortOrder === "desc"}
          onSort={() => sortData("solar_yield_yearly")} />
      </th>

      <th
        class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs text-gray-600 dark:text-les-white uppercase tracking-wider dark:bg-dark-table-header">
        Appliances
      </th>
    </tr>
  </thead>

  <tbody>
    {#each filteredData as data}
      <tr
        class="hover:!bg-gray-100 bg-white cursor-pointer text-sm hover:dark:!bg-dark-table-header dark:bg-dark-table-row dark:text-white"
        on:click={() => toggleRow(data.id)}>
        <td class="px-5 py-5">
          <button
            class="text-gray-800 cursor-pointer hover:text-blue-500 flex items-center gap-4 dark:text-les-white"
            on:click={() => ($activatedHousehold = data)}>
            {data.id}
          </button>
        </td>

        <td class="px-5 py-5">
          <button
            class="text-gray-800 cursor-pointer hover:text-blue-500 flex items-center gap-4 dark:text-les-white"
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
          class="bg-white hover:bg-white text-sm dark:bg-dark-table-row border-b border-gray-200 dark:border-les-white">
          <td colspan={7}>
            <div transition:slide class="p-4 flex justify-center">
              <SchedulableLoadGrid appliances={data.appliances} {hours} />
            </div>
          </td>
        </tr>
      {/if}

      {#if expandedRow !== data.id}
        <tr class="border-b border-gray-200"></tr>
      {/if}
    {/each}
  </tbody>
</table>
