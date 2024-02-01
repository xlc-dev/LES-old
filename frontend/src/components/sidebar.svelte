<script lang="ts">
  /*
   * The sidebar component contains the sidebar that is displayed in various other views.
   * The researcher can switch between the dashboard, simulation, and schedulable load views,
   * toggle the dark mode on or off, view the session options that were selected in the stepper,
   * and end the current session.
   */

  import { onMount, createEventDispatcher } from "svelte";

  import { stepperData } from "../lib/stores";

  export let currentComponent: string;

  const dispatch = createEventDispatcher();

  let isDarkMode = false;

  /**
   * Registers and handles button clicks by dispatching the corresponding event.
   * @param {string} action - The action triggered by the button click.
   */
  const handleButtonClick = (action: string) => {
    dispatch("click", { action });
    currentComponent = action;
  };

  /**
   * Triggers the function that turns dark mode on or off.
   * @returns {void}
   */
  const toggleDarkMode = () => {
    isDarkMode = !isDarkMode;
    updateDarkMode();
  };

  /**
   * Updates the dark mode setting and applies the corresponding styles to the document.
   * @returns {void}
   */
  const updateDarkMode = () => {
    // Save the dark mode setting to local storage
    localStorage.setItem("darkMode", isDarkMode.toString());

    if (isDarkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  };

  /*
   * Contains logic that runs at initialisation, as soon as the component has been mounted.
   * In this component it initialises the dark mode state at the start of a session based on the last saved state of a previous session.
   */
  onMount(() => {
    const savedDarkMode = localStorage.getItem("darkMode");
    isDarkMode = savedDarkMode === "true";
    updateDarkMode();
  });
</script>

<div class="fixed flex flex-col justify-between left-0 top-0 h-screen w-64 bg-gray-900">
  <div>
    <div class="w-full bg-dark-table-header p-4 flex gap-3 items-center">
      <img src="/arrows.png" alt="" class="transform rotate-180" />
      <p class="text-les-white">LES RESEARCH</p>
    </div>

    <div class="flex flex-col items-start justify-center gap-3 mt-4">
      <button
        class="flex items-center gap-3 hover:bg-les-sidebar-item w-full p-4 transition-colors duration-200 {currentComponent ===
        'Dashboard'
          ? 'bg-les-sidebar-item'
          : ''}"
        on:click={() => handleButtonClick("Dashboard")}>
        <img src="/rectangle.png" alt="" />
        <p class="text-les-white">Dashboard</p>
      </button>

      <button
        class="flex items-center gap-3 hover:bg-les-sidebar-item w-full p-4 transition-colors duration-200 {currentComponent ===
        'Simulation'
          ? 'bg-les-sidebar-item'
          : ''}"
        on:click={() => handleButtonClick("Simulation")}>
        <img src="/adjustment.png" alt="" />
        <p class="text-les-white">Simulation</p>
      </button>

      <button
        class="flex items-center gap-3 hover:bg-les-sidebar-item w-full p-4 transition-colors duration-200 {currentComponent ===
        'Schedulable Loads'
          ? 'bg-les-sidebar-item'
          : ''}"
        on:click={() => handleButtonClick("Schedulable Loads")}>
        <img src="/calendar.png" alt="" />
        <p class="text-les-white">Schedulable Loads</p>
      </button>
    </div>
  </div>

  <div class="mt-auto">
    <div class="px-4">
      <h3 class="text-lg font-semibold text-les-white pb-4">Selected Options:</h3>

      <p class="text-gray-400">Twin World: {$stepperData.twinworld.name}</p>
      <p class="text-gray-400">Cost Model: {$stepperData.costmodel.name}</p>
      <p class="text-gray-400">Algorithm: {$stepperData.algorithm.name}</p>

      <hr class="border-gray-800 my-4" />

      <div class="flex items-center pb-4">
        <label for="dark-mode-toggle" class="mr-2 text-les-white"
          >{isDarkMode ? "Dark Mode" : "Light Mode"}</label>
        <input
          type="checkbox"
          id="dark-mode-toggle"
          class="hidden"
          checked={isDarkMode}
          on:change={toggleDarkMode} />
        <label for="dark-mode-toggle" class="cursor-pointer">
          <div class="relative">
            <div
              class={`block w-14 h-8 rounded-full ${isDarkMode ? "bg-les-blue" : "bg-gray-600"}`}>
            </div>
            <div
              class={`absolute left-1 top-1 bg-white w-6 h-6 rounded-full transition ${
                isDarkMode ? "transform translate-x-full" : ""
              }`}>
            </div>
          </div>
        </label>
      </div>
    </div>

    <button
      class="flex items-center gap-3 hover:brightness-110 bg-les-red-dark w-full p-4 py-6 transition-colors duration-200"
      on:click={() => handleButtonClick("Stop")}>
      <img src="/stop.png" alt="" />
      <p class="text-les-white">Stop Simulation</p>
    </button>
  </div>
</div>
