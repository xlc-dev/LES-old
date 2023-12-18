<script lang="ts">
  import { stepperData } from "../lib/stores";

  const showHome = () => {};
</script>

<div class="grid grid-cols-5 gap-4">
  {#each $stepperData as data}
    <button class="text-gray-800 cursor-pointer hover:text-blue-500" on:click={showHome}
      >{data.name}</button>
  {/each}
</div>
