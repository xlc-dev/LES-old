<script lang="ts">
  import { blur } from "svelte/transition";

  import Sidebar from "./sidebar.svelte";
  import SchedulableLoadTable from "./schedulableLoadTable.svelte";
  import Simulation from "./simulation.svelte";

  let selectedComponent = null;

  const handleButtonClick = (action) => {
    switch (action) {
      case "Dashboard":
        selectedComponent = null;
        break;
      case "Simulation":
        selectedComponent = Simulation;
        break;
      case "SchedulableLoads":
        selectedComponent = SchedulableLoadTable;
        break;
      case "StockMarket":
        selectedComponent = null;
        break;
      case "Stop":
        selectedComponent = null;
        break;
    }
  };
</script>

<Sidebar on:click={(e) => handleButtonClick(e.detail.action)} />
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
