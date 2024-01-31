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
   * @param {number} bitmap - The bitmap value to determine the color from.
   * @param {number} hour - The hour for which the color is being determined.
   * @param {string} selectedDate - The selected date for which the color is being determined.
   * @param {number} appliance_id - The ID of the appliance for which the color is being determined.
   * @returns {string} - The background color class name ("bg-blue-600", "bg-gray-700", "bg-green-500", or "bg-red-500").
   */
  const getCellColor = (
    bitmap: number,
    hour: number,
    selectedDate: string,
    appliance_id: number
  ) => {
    const bitmapString = bitmap.toString(2).padStart(24, "0");

    // Convert the startDate from Unix timestamp to Date
    const baseDate = new Date($startDate * 1000);

    // Ensure selectedDate is a Date object
    const dateObj = new Date(selectedDate);
    // Set the time to midnight
    dateObj.setHours(0, 0, 0, 0);

    // Calculate the day number based on the selected date and start date
    const dayNumber = Math.round(
      (dateObj.getTime() - (baseDate.getTime() - 1 * 60 * 60 * 1000)) / (24 * 60 * 60 * 1000)
    );

    // Find the corresponding day in timeDailies based on the calculated day number
    const dayData = $timeDailies.filter(
      (entry) => entry.id === 304 * (appliance_id - 1) + dayNumber + 1
    );

    // Fallback if user hasn't selected a date that has no timeDailies
    if (dayData.length === 0) {
      return "bg-gray-700";
    }

    const planEnergyBit = (dayData[0].bitmap_plan_energy >> (23 - hour)) & 1;
    const planNoEnergyBit = (dayData[0].bitmap_plan_no_energy >> (23 - hour)) & 1;

    if (planEnergyBit === 1) {
      if (bitmapString[hour] !== "1") {
        return "bg-yellow-700";
      }
      return "bg-green-700"; // Green for energy from solar panels
    } else if (planNoEnergyBit === 1) {
      if (bitmapString[hour] !== "1") {
        return "bg-les-red-dark";
      }
      return "bg-les-red"; // Red for energy from the national grid
    }

    // Default to gray for unavailable time slots
    return bitmapString[hour] === "1" ? "bg-les-blue" : "bg-gray-700";
  };

  /**
   * Calculates the grid size class based on the current window width.
   * @returns {string} The grid size class.
   */
  const getGridSizeClass = () => {
    const breakpoints = {
      '2xl': 1536,
      'xl': 1280,
      'lg': 1024,
      'md': 768,
      'sm': 640,
    };

    const screenWidth = window.innerWidth;

    if (screenWidth >= breakpoints['2xl']) {
      return 'w-8 h-8';
    } else if (screenWidth >= breakpoints['xl']) {
      return 'w-7 h-7';
    } else if (screenWidth >= breakpoints['lg']) {
      return 'w-6 h-6';
    } else if (screenWidth >= breakpoints['md']) {
      return 'w-5 h-5';
    } else {
      return 'w-4 h-4';
    }
  };

  let gridSizeClass = getGridSizeClass();

  window.addEventListener('resize', () => {
    gridSizeClass = getGridSizeClass();
  });

  /**
   * Converts a given Date object to a Unix timestamp.
   * @param {Date} date - The Date object to convert.
   * @returns {number} - The Unix timestamp of the given date.
   */
  $: unixTimestamp = Math.floor(dateNoFormat.getTime() / 1000);
</script>

<div class="flex flex-col items-center">
  <div class="flex w-full justify-start">
    <div class="w-36 text-right pr-2 font-bold dark:text-les-white text-xs">Appliances:</div>
    <div class="flex">
      {#each hours as hour}
        <div class="w-2 h-2 sm:w-3 sm:h-3 md:w-4 md:h-4 text-center dark:text-les-white text-xs">{hour}</div>
      {/each}
    </div>
  </div>
  {#each appliances as appliance}
    <div class="flex items-center">
      <div class="w-36 text-right pr-2 whitespace-nowrap dark:text-les-white text-xs">
        {appliance.name}
      </div>
      {#each hours as hour}
        <div
          class={`border border-white ${getCellColor(
            appliance.appliance_windows[(Math.round(unixTimestamp / 86400) + 3) % 7].bitmap_window,
            hour,
            date,
            appliance.id
          )} w-2 h-2 sm:w-3 sm:h-3 md:w-4 md:h-4`}>
        </div>
      {/each}
    </div>
  {/each}
</div>
