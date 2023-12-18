<script lang="ts">
  import {stepperData, twdata} from "../lib/stores";
  console.log($stepperData);

  function handleButtonClick(action) {
    console.log(`Button clicked: ${action}`);

  }
</script>
<!--&lt;!&ndash;      To view the ids of all the households in the current twin world:&ndash;&gt;-->
<!--      {#each $stepperData as data}-->
<!--        <p>{data.id}</p>-->
<!--      {/each}-->
<!--    </div>-->
<!--  </div>-->

<div class="flex">
  <div class="w-64 bg-les-bg h-screen p-4">
    <div class="flex flex-col">
      <button class="mb-2 p-2 bg-blue-500 text-white" on:click={() => handleButtonClick('Action1')}>Dashboard</button>
      <button class="mb-2 p-2 bg-blue-500 text-white" on:click={() => handleButtonClick('Action2')}>Simulation</button>
      <button class="mb-2 p-2 bg-blue-500 text-white" on:click={() => handleButtonClick('Action3')}>Schedulable loads</button>
      <button class="mb-2 p-2 bg-blue-500 text-white" on:click={() => handleButtonClick('Action4')}>Stock market</button>
    </div>
    <div class="flex flex-col">
    </div>
    <div class="mt-auto fixed bottom-0">
      <h3 class="text-lg font-semibold text-white">Selected Options:</h3>
      <p class="text-white">Twin World: {$twdata.twin_world || 'Not selected'}</p>
      <p class="text-white">Cost Model: {$twdata.cost_model || 'Not selected'}</p>
      <p class="text-white">Algorithm: {$twdata.algorithm || 'Not selected'}</p>
    </div>
  </div>
  <div class="flex-1 bg-les-frame">
  </div>
</div>
