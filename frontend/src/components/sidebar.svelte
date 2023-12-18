<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import { twdata } from "../lib/stores";

  const dispatch = createEventDispatcher();

  const handleButtonClick = (action) => {
    dispatch("click", { action });
  };
</script>

<div class="fixed flex flex-col justify-between left-0 top-0 h-screen w-64 p-4 bg-gray-900">
  <div class="flex flex-col">
    <button class="mb-2 p-2 bg-blue-500 text-white" on:click={() => handleButtonClick("Dashboard")}
      >Dashboard</button>
    <button
      class="mb-2 p-2 bg-blue-500 text-white"
      on:click={() => handleButtonClick("Simulation")}>Simulation</button>
    <button
      class="mb-2 p-2 bg-blue-500 text-white"
      on:click={() => handleButtonClick("SchedulableLoads")}>Schedulable loads</button>
    <button
      class="mb-2 p-2 bg-blue-500 text-white"
      on:click={() => handleButtonClick("StockMarket")}>Stock market</button>
  </div>
  <div>
    <h3 class="text-lg font-semibold text-white pb-4">Selected Options:</h3>
    <p class="text-gray-400">Twin World: {$twdata.twin_world}</p>
    <p class="text-gray-400">Cost Model: {$twdata.cost_model}</p>
    <p class="text-gray-400">Algorithm: {$twdata.algorithm}</p>
    <hr class="border-gray-800 my-4" />
    <button
      class="mb-2 p-2 bg-blue-500 text-white w-full"
      on:click={() => handleButtonClick("Stop")}>Stop</button>
  </div>
</div>
