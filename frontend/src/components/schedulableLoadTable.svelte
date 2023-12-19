<script lang="ts">
  import { stepperData } from "../lib/stores";
  import { get } from 'svelte/store';

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

  let filteredData = get(stepperData);

  function applyFilters() {
    let isAnyFilterSelected = Object.values(selectedFilters).some(filter => filter.length > 0);
    if (!isAnyFilterSelected) {
      filteredData = get(stepperData);
      return;
    }

    filteredData = get(stepperData).filter(item => {
      let matchesSize = selectedFilters.size.length === 0 || selectedFilters.size.includes(item.size);
      let matchesEnergyUsage = selectedFilters.energyUsage.length === 0 || selectedFilters.energyUsage.some(range => item.energy_usage >= range.min && item.energy_usage < range.max);
      let matchesSolarPanels = selectedFilters.solarPanels.length === 0 || selectedFilters.solarPanels.includes(item.solar_panels);
      let matchesSolarYieldYearly = selectedFilters.solarYieldYearly.length === 0 || selectedFilters.solarYieldYearly.some(range => item.solar_yield_yearly >= range.min && item.solar_yield_yearly < range.max);
      let matchesAppliances = selectedFilters.appliances.length === 0 || item.appliances.some(appliance => selectedFilters.appliances.includes(appliance.name));

      return matchesSize && matchesEnergyUsage && matchesSolarPanels && matchesSolarYieldYearly && matchesAppliances;
    });
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

<div class="filter-bar">
  {#each Object.entries(filters) as [filterName, options]}
    <div class="dropdown">
      <button>{filterName}</button>
      <div class="dropdown-content">
        {#each options as option}
          <label>
            <input type="checkbox" bind:group={selectedFilters[filterName]} value={option}>
            {typeof option === 'object' ? `${option.min}-${option.max}` : option}
          </label>
        {/each}
      </div>
    </div>
  {/each}
  <button on:click={applyFilters}>Apply Filters</button>
</div>

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
