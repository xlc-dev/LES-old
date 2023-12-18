<script lang="ts">
  import type { HouseholdRead } from "../lib/client";
  import { stepperData } from "../lib/stores";

  import HomeView from "./homeView.svelte";

  let household: HouseholdRead;

  $: selectedHousehold = household;

  const showHome = (data: HouseholdRead) => {
    household = data;
  };
</script>

{#if !selectedHousehold}
  <div class="grid grid-cols-5 gap-4">
    {#each $stepperData as data}
      <button
        class="text-gray-800 cursor-pointer hover:text-blue-500 flex items-center gap-4"
        on:click={() => showHome(data)}>
        <img src="/house.svg" class="h-6" alt="" />
        {data.name}
      </button>
    {/each}
  </div>
{:else}
  <HomeView {household} />
{/if}
