<script lang="ts">
  import { blur } from "svelte/transition";

  import Sidebar from "./sidebar.svelte";
  import TitleBar from "./titleBar.svelte";
  import Result from "./result.svelte";
  import SchedulableLoadTable from "./schedulableLoadTable.svelte";
  import Simulation from "./simulation.svelte";

  let selectedComponent = null;
  let title = "Dashboard";
  let stop = false;

  const handleButtonClick = (action: string) => {
    switch (action) {
      case "Dashboard":
        selectedComponent = null;
        title = "Dashboard";
        break;
      case "Simulation":
        selectedComponent = Simulation;
        title = "Simulation";
        break;
      case "SchedulableLoads":
        selectedComponent = SchedulableLoadTable;
        title = "Schedulable Loads";
        break;
      case "StockMarket":
        selectedComponent = null;
        title = "Stock Market";
        break;
      case "Stop":
        stop = true;
        break;
    }
  };
</script>

{#if !stop}
  <Sidebar on:click={(e) => handleButtonClick(e.detail.action)} />
  <TitleBar {title} />
  <main class="flex-1 bg-les-frame ml-64 p-4 min-h-screen" in:blur>
    {#if selectedComponent !== null}
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
