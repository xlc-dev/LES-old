<script lang="ts">
  /*
  The schedulableLoadGrid component contains the grid raster that is used in each card of the
  schedulable load table and in the view of each individual household. The x-axis of the grid
  raster contains the hours of the day and the y-axis contains the appliances of a household.
  The gray boxes contain the time slots that are unavailable to plan appliances in. The blue
  boxes contain the time slots that are available. The red and green boxes contain the time
  slots that are planned in. The green boxes indicate that the energy used is drawn from solar
  panels, while the red boxes indicate that the energy used is drawn from the national grid.
  */

  import type { ApplianceRead_Output } from "../lib/client";

  export let appliances: ApplianceRead_Output[];
  export let hours: number[];

  // Determines the color of a box in a schedulable load grid raster based on a bitmap value
  const getCellColor = (bitmap: number, hour: number) => {
    const bitmapString = bitmap.toString(2).padStart(24, "0");
    return bitmapString[hour] === "1" ? "bg-blue-600" : "bg-gray-700";
  };
</script>

<div class="flex flex-col items-center">
  <div class="flex w-full justify-start">
    <div class="w-36 text-right pr-2 font-bold dark:text-les-white">Appliances:</div>
    <div class="flex">
      {#each hours as hour}
        <div class="w-6 h-6 text-center dark:text-les-white">{hour}</div>
      {/each}
    </div>
  </div>
  {#each appliances as appliance}
    <div class="flex items-center">
      <div class="w-36 text-right pr-2 whitespace-nowrap dark:text-les-white">
        {appliance.name}
      </div>
      {#each hours as hour}
        <div
          class={`w-6 h-6 border border-white ${getCellColor(
            appliance.appliance_windows[0].bitmap_window,
            hour
          )}`}>
        </div>
      {/each}
    </div>
  {/each}
</div>
