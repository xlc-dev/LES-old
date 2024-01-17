<script lang="ts">
  /*
  The baseLayout component handles the actions that form the application's navigational flow.
  It also imports individual components so that they can be used throughout the application.
  Finally, it also ensures that some components, such as the sidebar, persist in multiple views.
  */

  import { blur } from "svelte/transition";

  import { activatedHousehold } from "../lib/stores";

  import Sidebar from "./sidebar.svelte";
  import TitleBar from "./titleBar.svelte";
  import Result from "./result.svelte";
  import SchedulableLoadTable from "./schedulableLoadTable.svelte";
  import Simulation from "./simulation.svelte";
  import Dashboard from "./dashboard.svelte";
  import Household from "./household.svelte";

  let selectedComponent = null;
  let title = "Schedulable Loads";
  let stop = false;

  let unsubscribe: () => void;

  // Navigates to a different view based on the button that was clicked
  const handleButtonClick = (action: string) => {
    if (unsubscribe) unsubscribe();

    $activatedHousehold = null;

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

  <main class="flex-1 bg-light-les-frame dark:bg-dark-les-bg ml-64 p-4 min-h-screen" in:blur>
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
      <SchedulableLoadTable />
    {/if}
  </main>
{:else}
  <Result />
{/if}
