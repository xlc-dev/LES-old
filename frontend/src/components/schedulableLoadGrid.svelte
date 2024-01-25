<script lang="ts">
  /*
   * The schedulableLoadGrid component contains the grid raster that is used in each card of the
   * schedulable load table and in the view of each individual household. The x-axis of the grid
   * raster contains the hours of the day and the y-axis contains the appliances of a household.
   * The gray boxes contain the time slots that are unavailable to plan appliances in. The blue
   * boxes contain the time slots that are available. The red and green boxes contain the time
   * slots that are planned in. The green boxes indicate that the energy used is drawn from solar
   * panels, while the red boxes indicate that the energy used is drawn from the national grid.
   */

  import type { ApplianceRead_Output } from "../lib/client";

  import { timeDailies, startDate } from "../lib/stores";

  export let appliances: ApplianceRead_Output[];
  export let hours: number[];
  export let date: string;
  export let dateNoFormat: Date;

  /**
   * Determines the color of a box in a schedulable load grid raster based on a bitmap value.
   *
   * @param {number} bitmap - The bitmap value to determine the color from.
   * @param {number} hour - The hour for which the color is being determined.
   * @param {Date} selectedDate - The selected date for which the color is being determined.
   * @param {number} appliance_id - The ID of the appliance for which the color is being determined.
   * @returns {string} - The background color class name ("bg-blue-600", "bg-gray-700", "bg-green-500", or "bg-red-500").
   */
  const getCellColor = (bitmap, hour, selectedDate, appliance_id) => {
    const bitmapString = bitmap.toString(2).padStart(24, "0");

    // Convert the startDate from Unix timestamp to Date
    const baseDate = new Date($startDate * 1000);

    // Ensure selectedDate is a Date object
    const dateObj = new Date(selectedDate);
    // Set the time to midnight
    dateObj.setHours(0, 0, 0, 0);

    // Calculate the day number based on the selected date and start date
    const dayNumber =
      Math.floor((dateObj.getTime() - (baseDate.getTime() - 60 * 60 * 1000)) / (24 * 60 * 60 * 1000));

    console.log(dayNumber);

    // Find the corresponding day in timeDailies based on the calculated day number
    const dayData = $timeDailies.filter(
      (entry) => entry.id === 304 * (appliance_id - 1) + dayNumber
    );

    // Fallback if user hasn't selected a date that has no timeDailies
    if (dayData.length === 0) {
      return "bg-gray-700";
    }

    const planEnergyBit = (dayData[0].bitmap_plan_energy >> (23 - hour)) & 1;
    const planNoEnergyBit = (dayData[0].bitmap_plan_no_energy >> (23 - hour)) & 1;

    if (planEnergyBit === 1) {
      if (bitmapString[hour] !== "1") {
        return "bg-yellow-500";
      }
      return "bg-green-500"; // Green for energy from solar panels
    } else if (planNoEnergyBit === 1) {
      if (bitmapString[hour] !== "1") {
        return "bg-les-red-dark";
      }
      return "bg-red-500"; // Red for energy from the national grid
    }

    // Default to gray for unavailable time slots
    return bitmapString[hour] === "1" ? "bg-blue-600" : "bg-gray-700";
  };

  $: unixTimestamp = Math.floor(dateNoFormat.getTime() / 1000);
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
            appliance.appliance_windows[(Math.floor(unixTimestamp / 86400) + 3) % 7].bitmap_window,
            hour,
            date,
            appliance.id
          )}`}>
        </div>
      {/each}
    </div>
  {/each}
</div>
