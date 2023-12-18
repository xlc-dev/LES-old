<script lang="ts">
  import { stepperData } from "../lib/stores";

  function formatAppliances(appliances) {
    return appliances
      .map(
        (appliance) =>
          `${appliance.name} (Power: ${appliance.power}, Duration: ${appliance.duration})`
      )
      .join(", ");
  }
</script>

<table class="min-w-full leading-normal">
  <thead>
    <tr>
      <th
        class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
        ID
      </th>
      <th
        class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
        Name
      </th>
      <th
        class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
        Size
      </th>
      <th
        class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
        Energy Usage
      </th>
      <th
        class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
        Solar Panels
      </th>
      <th
        class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
        Solar Yield Yearly
      </th>
      <th
        class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
        Appliances
      </th>
    </tr>
  </thead>
  <tbody>
    {#each $stepperData as data}
      <tr>
        <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
          {data.id}
        </td>
        <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
          {data.name}
        </td>
        <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
          {data.size}
        </td>
        <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
          {data.energy_usage}
        </td>
        <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
          {data.solar_panels}
        </td>
        <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
          {data.solar_yield_yearly}
        </td>
        <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
          {formatAppliances(data.appliances)}
        </td>
      </tr>
    {/each}
  </tbody>
</table>
