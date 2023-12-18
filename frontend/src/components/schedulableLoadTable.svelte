<script lang="ts">
  import { stepperData } from "../lib/stores";

  let sortColumn = null;
  let sortOrder = 'asc';

  function sortData(column) {
    sortColumn = column;
    stepperData.update(data => {
      return data.slice().sort((a, b) => {
        if (a[column] < b[column]) return sortOrder === 'asc' ? -1 : 1;
        if (a[column] > b[column]) return sortOrder === 'asc' ? 1 : -1;
        return 0;
      });
    });
    sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
  }

  function formatAppliances(appliances) {
    return appliances.map(appliance => `${appliance.name} (Power: ${appliance.power}, Duration: ${appliance.duration})`).join(', ');
  }
</script>

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
    {#each $stepperData as data}
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
