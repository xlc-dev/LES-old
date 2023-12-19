<script lang="ts">
  import { stepperData } from "../lib/stores";
  import { get } from 'svelte/store';
  import { fade, slide } from 'svelte/transition';

  let sortColumn = null;
  let sortOrder = 'asc';

  let filters = {
    size: Array.from({ length: 10 }, (_, i) => i + 1),
    energyUsage: Array.from({ length: 10 }, (_, i) => ({ min: i * 1000, max: (i + 1) * 1000 })),
    solarPanels: Array.from({ length: 21 }, (_, i) => i),
    solarYieldYearly: Array.from({ length: 10 }, (_, i) => ({ min: i * 1000, max: (i + 1) * 1000 })),
    appliances: ['Dishwasher', 'Washing Machine', 'Tumble Dryer', 'Stove', 'Electric Vehicle']
  };

  let selectedFilters = {
    size: [],
    energyUsage: [],
    solarPanels: [],
    solarYieldYearly: [],
    appliances: []
  };

  let filteredData = [];

  $: {
    let data = get(stepperData);
    filteredData = data.filter(item => {
      let matchesSize = selectedFilters.size.length === 0 || selectedFilters.size.includes(item.size);
      let matchesEnergyUsage = selectedFilters.energyUsage.length === 0 || selectedFilters.energyUsage.some(range => item.energy_usage >= range.min && item.energy_usage < range.max);
      let matchesSolarPanels = selectedFilters.solarPanels.length === 0 || selectedFilters.solarPanels.includes(item.solar_panels);
      let matchesSolarYieldYearly = selectedFilters.solarYieldYearly.length === 0 || selectedFilters.solarYieldYearly.some(range => item.solar_yield_yearly >= range.min && item.solar_yield_yearly < range.max);
      let matchesAppliances = selectedFilters.appliances.length === 0 || item.appliances.some(appliance => selectedFilters.appliances.includes(appliance.name));

      return matchesSize && matchesEnergyUsage && matchesSolarPanels && matchesSolarYieldYearly && matchesAppliances;
    });
  }

  let showDropdown = null;
  function toggleDropdown(filterName) {
    showDropdown = showDropdown === filterName ? null : filterName;
  }

  function createHandleClickOutside(filterName) {
    return function(event) {
      if (!event.target.closest(`#${filterName}-dropdown`)) {
        showDropdown = null;
      }
    };
  }

  function toReadableName(camelCase) {
    return camelCase
            // Insert a space before all caps
            .replace(/([A-Z])/g, ' $1')
            // Uppercase the first character
            .replace(/^./, str => str.toUpperCase());
  }

  function sortData(column) {
    sortColumn = column;
    filteredData = filteredData.slice().sort((a, b) => {
      if (a[column] < b[column]) return sortOrder === 'asc' ? -1 : 1;
      if (a[column] > b[column]) return sortOrder === 'asc' ? 1 : -1;
      return 0;
    });
    sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
  }
</script>

<div class="flex justify-between items-center rounded-lg bg-gray-100 p-2">
  <div class="flex space-x-4">
    {#each Object.entries(filters) as [filterName, options]}
      <div class="relative" id={`${filterName}-dropdown`} on:click|stopPropagation={createHandleClickOutside(filterName)}>
        <button class="px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50" on:click={() => toggleDropdown(filterName)} on:keydown={(e) => e.key === 'Enter' && toggleDropdown(filterName)}>
          {toReadableName(filterName)}
        </button>
        {#if showDropdown === filterName}
          <div class="absolute left-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-10" in:slide={{ duration: 750 }} out:slide={{ duration: 750 }}>
            <div class="py-1">
              {#each options as option}
                <label class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                  <input type="checkbox" class="mr-2" bind:group={selectedFilters[filterName]} value={option} on:change={() => {}}>
                  {typeof option === 'object' ? `${option.min}-${option.max}` : option}
                </label>
              {/each}
            </div>
          </div>
        {/if}
      </div>
    {/each}
  </div>
</div>

<br>

<table class="min-w-full leading-normal rounded-lg overflow-hidden">
  <thead>
    <tr>
      <th
        class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
        ID
        <button on:click={() => sortData('id')}>Sort</button>
      </th>
      <th
        class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
        Name
        <button on:click={() => sortData('name')}>Sort</button>
      </th>
      <th
        class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
        Size
      </th>
      <th
        class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
        Energy Usage
        <button on:click={() => sortData('energy_usage')}>Sort</button>
      </th>
      <th
        class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
        Solar Panels
        <button on:click={() => sortData('solar_panels')}>Sort</button>
      </th>
      <th
        class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
        Solar Yield Yearly
        <button on:click={() => sortData('solar_yield_yearly')}>Sort</button>
      </th>
      <th
        class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
        Appliances
      </th>
    </tr>
  </thead>
  <tbody>
    {#each filteredData as data}
      <tr class="hover:!bg-les-frame bg-white cursor-pointer text-sm">
        <td class="px-5 py-5 border-b border-gray-200">
          {data.id}
        </td>
        <td class="px-5 py-5 border-b border-gray-200">
          {data.name}
        </td>
        <td class="px-5 py-5 border-b border-gray-200">
          {data.size}
        </td>
        <td class="px-5 py-5 border-b border-gray-200">
          {data.energy_usage}
        </td>
        <td class="px-5 py-5 border-b border-gray-200">
          {data.solar_panels}
        </td>
        <td class="px-5 py-5 border-b border-gray-200">
          {data.solar_yield_yearly}
        </td>
        <td class="px-5 py-5 border-b border-gray-200">
          {#each data.appliances as appliance}
          {appliance.name}
            <br>
          {/each}
        </td>
      </tr>
    {/each}
  </tbody>
</table>
