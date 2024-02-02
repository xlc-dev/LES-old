<script lang="ts">
  /**
   * The baseLayout component handles the actions that form the application's navigational flow.
   * It also imports individual components so that they can be used throughout the application.
   * Finally, it also ensures that some components, such as the sidebar, persist in multiple views.
   */

  import { createEventDispatcher } from "svelte";
  import { blur } from "svelte/transition";

  import { activatedHousehold } from "../lib/stores";

  import Sidebar from "./sidebar.svelte";
  import TitleBar from "./titleBar.svelte";
  import Result from "./result.svelte";
  import SchedulableLoadTable from "./schedulableLoadTable.svelte";
  import Simulation from "./simulation.svelte";
  import Dashboard from "./dashboard.svelte";
  import Household from "./household.svelte";

  const dispatch = createEventDispatcher();

  let unsubscribe: () => void;

  let selectedComponent = null;
  let title = "Dashboard";
  let stop = false;

  /**
   * Navigates to a different view based on the button that was clicked.
   *
   * @param {string} action - The action associated with the clicked button.
   */
  const handleButtonClick = (action: string) => {
    // Unsubscribe if previously subscribed
    if (unsubscribe) unsubscribe();

    // Reset activated household
    $activatedHousehold = null;

    // Determine the selected component and title based on the action
    switch (action) {
      case "Dashboard":
        selectedComponent = Dashboard;
        title = "Dashboard";
        break;
      case "Simulation":
        selectedComponent = Simulation;
        title = "Simulation";
        break;
      case "Schedulable Loads":
        selectedComponent = SchedulableLoadTable;
        title = "Schedulable Loads";
        break;
      case "Stop":
        stop = true;
        dispatch("stop");
        break;
    }
  };

  // Changes the name of the title bar based on the currently selected household
  $: if ($activatedHousehold != null) {
    unsubscribe = activatedHousehold.subscribe((e) => {
      title = e.name;
    });
  }
</script>

{#if !stop}
  <Sidebar on:click={(e) => handleButtonClick(e.detail.action)} currentComponent={title} />
  <TitleBar {title} />

  <main class="ml-64 min-h-screen flex-1 bg-les-gray-200 p-4 dark:bg-les-gray-500" in:blur>
    {#if $activatedHousehold !== null}
      <Household household={$activatedHousehold} />
    {:else if selectedComponent !== null}
      <div in:blur>
        {#key selectedComponent}
          <div in:blur>
            <svelte:component this={selectedComponent} />
          </div>
        {/key}
      </div>
    {:else}
      <Dashboard />
    {/if}
  </main>
{:else}
  <Result />
{/if}
