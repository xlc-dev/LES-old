<script lang="ts">
  /**
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

  /**
   * Contains logic that runs at initialisation, as soon as the component has been mounted.
   * In this component it initialises the dark mode state at the start of a session based on the last saved state of a previous session.
   */
  onMount(() => {
    const savedDarkMode = localStorage.getItem("darkMode");
    isDarkMode = savedDarkMode === "true";
    updateDarkMode();
  });
</script>

<div class="fixed left-0 top-0 flex h-screen w-64 flex-col justify-between bg-gray-900">
  <div>
    <div class="flex w-full items-center gap-3 bg-les-gray-700 p-4">
      <img src="/arrows.png" alt="" class="rotate-180 transform" />
      <p class="text-les-white">LES RESEARCH</p>
    </div>

    <div class="mt-4 flex flex-col items-start justify-center gap-3">
      <button
        class="flex w-full items-center gap-3 p-4 transition-colors duration-200 hover:bg-les-gray-700 {currentComponent ===
        'Dashboard'
          ? 'bg-les-gray-700'
          : ''}"
        on:click={() => handleButtonClick("Dashboard")}>
        <img src="/rectangle.png" alt="" />
        <p class="text-les-white">Dashboard</p>
      </button>

      <button
        class="flex w-full items-center gap-3 p-4 transition-colors duration-200 hover:bg-les-gray-700 {currentComponent ===
        'Simulation'
          ? 'bg-les-gray-700'
          : ''}"
        on:click={() => handleButtonClick("Simulation")}>
        <img src="/adjustment.png" alt="" />
        <p class="text-les-white">Simulation</p>
      </button>

      <button
        class="flex w-full items-center gap-3 p-4 transition-colors duration-200 hover:bg-les-gray-700 {currentComponent ===
        'Schedulable Loads'
          ? 'bg-les-gray-700'
          : ''}"
        on:click={() => handleButtonClick("Schedulable Loads")}>
        <img src="/calendar.png" alt="" />
        <p class="text-les-white">Schedulable Loads</p>
      </button>
    </div>
  </div>

  <div class="mt-auto">
    <div class="px-4">
      <h3 class="pb-4 text-lg font-semibold text-les-white">Selected Options:</h3>

      <p class="text-gray-400">Twin World: {$stepperData.twinworld.name}</p>
      <p class="text-gray-400">Cost Model: {$stepperData.costmodel.name}</p>
      <p class="text-gray-400">Algorithm: {$stepperData.algorithm.name}</p>

      <hr class="my-4 border-gray-800" />

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
              class={`block h-8 w-14 rounded-full ${isDarkMode ? "bg-les-blue" : "bg-gray-600"}`}>
            </div>
            <div
              class={`absolute left-1 top-1 h-6 w-6 rounded-full bg-white transition ${
                isDarkMode ? "translate-x-full transform" : ""
              }`}>
            </div>
          </div>
        </label>
      </div>
    </div>

    <button
      id="stop-button"
      class="flex w-full items-center gap-3 bg-les-red-dark p-4 py-6 transition-colors duration-200 hover:brightness-110"
      on:click={() => handleButtonClick("Stop")}>
      <img src="/stop.png" alt="" />
      <p class="text-les-white">Stop Simulation</p>
    </button>
  </div>
</div>
