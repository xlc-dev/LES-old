<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import { twdata } from "../lib/stores";

  const dispatch = createEventDispatcher();
  let currentComponent = "SchedulableLoads";

  const handleButtonClick = (action) => {
    dispatch("click", { action });
    currentComponent = action;
  };
</script>

<div class="fixed flex flex-col justify-between left-0 top-0 h-screen w-64 bg-gray-900">
  <div>
    <div class="w-full bg-les-bg-dark p-4 flex gap-3 items-center">
      <img src="/arrows.png" alt="" class="transform rotate-180" />
      <p class="text-les-frame">LES RESEARCH</p>
    </div>
    <div class="flex flex-col items-start justify-center gap-3 mt-4">
      <button
        class="flex items-center gap-3 hover:bg-les-bg-dark w-full p-4 transition-colors duration-200 {currentComponent ===
        'Dashboard'
          ? 'bg-les-bg-dark hover:!bg-les-bg'
          : ''}"
        on:click={() => handleButtonClick("Dashboard")}>
        <img src="/rectangle.png" alt="" />
        <p class="text-les-frame">Dashboard</p>
      </button>
      <button
        class="flex items-center gap-3 hover:bg-les-bg-dark w-full p-4 transition-colors duration-200 {currentComponent ===
        'Simulation'
          ? 'bg-les-bg-dark hover:!bg-les-bg'
          : ''}"
        on:click={() => handleButtonClick("Simulation")}>
        <img src="/adjustment.png" alt="" />
        <p class="text-les-frame">Simulation</p>
      </button>
      <button
        class="flex items-center gap-3 hover:bg-les-bg-dark w-full p-4 transition-colors duration-200 {currentComponent ===
        'SchedulableLoads'
          ? 'bg-les-bg-dark hover:!bg-les-bg'
          : ''}"
        on:click={() => handleButtonClick("SchedulableLoads")}>
        <img src="/calendar.png" alt="" />
        <p class="text-les-frame">Schedulable Loads</p>
      </button>
      <button
        class="flex items-center gap-3 hover:bg-les-bg-dark w-full p-4 transition-colors duration-200 {currentComponent ===
        'StockMarket'
          ? 'bg-les-bg-dark hover:!bg-les-bg'
          : ''}"
        on:click={() => handleButtonClick("StockMarket")}>
        <img src="/money.png" alt="" />
        <p class="text-les-frame">Stock Market</p>
      </button>
    </div>
  </div>
  <div class="mt-auto">
    <div class="px-4">
      <h3 class="text-lg font-semibold text-les-frame pb-4">Selected Options:</h3>
      <p class="text-gray-400">Twin World: {$twdata.twin_world}</p>
      <p class="text-gray-400">Cost Model: {$twdata.cost_model}</p>
      <p class="text-gray-400">Algorithm: {$twdata.algorithm}</p>
      <hr class="border-gray-800 my-4" />
    </div>
    <button
      class="flex items-center gap-3 hover:bg-les-bg-dark bg-les-red-dark w-full p-4 py-6 transition-colors duration-200"
      on:click={() => handleButtonClick("Stop")}>
      <img src="/stop.png" alt="" />
      <p class="text-les-frame">Stop Simulation</p>
    </button>
  </div>
</div>
