<script lang="ts">
  import {stepperData, twdata} from "../lib/stores";
  console.log($stepperData);

  // Function to handle button clicks (modify as needed)
  function handleButtonClick(action) {
    console.log(`Button clicked: ${action}`);

  }
</script>

<!--<div class="flex">-->
<!--  &lt;!&ndash; Sidebar &ndash;&gt;-->
<!--  <div class="w-64 h-screen bg-gray-200 p-4">-->
<!--    &lt;!&ndash; Buttons at the top &ndash;&gt;-->
<!--    <div class="flex flex-col">-->
<!--      <button class="mb-2 p-2 bg-blue-500 text-white" on:click={() => handleButtonClick('Action1')}>Button 1</button>-->
<!--      <button class="mb-2 p-2 bg-blue-500 text-white" on:click={() => handleButtonClick('Action2')}>Button 2</button>-->
<!--      <button class="mb-2 p-2 bg-blue-500 text-white" on:click={() => handleButtonClick('Action3')}>Button 3</button>-->
<!--      <button class="mb-2 p-2 bg-blue-500 text-white" on:click={() => handleButtonClick('Action4')}>Button 4</button>-->
<!--    </div>-->

<!--    &lt;!&ndash; Selected options at the bottom &ndash;&gt;-->
<!--    <div class="mt-auto">-->
<!--      <h3 class="text-lg font-semibold">Selected Options:</h3>-->
<!--&lt;!&ndash;      <p>Twin World: {$stepperData.twin_world}</p>&ndash;&gt;-->
<!--&lt;!&ndash;      <p>Cost Model: {$stepperData.cost_model}</p>&ndash;&gt;-->
<!--&lt;!&ndash;      <p>Algorithm: {$stepperData.algorithm}</p>&ndash;&gt;-->

<!--&lt;!&ndash;      To view the ids of all the households in the current twin world:&ndash;&gt;-->
<!--      {#each $stepperData as data}-->
<!--        <p>{data.id}</p>-->
<!--      {/each}-->
<!--    </div>-->
<!--  </div>-->

<div class="flex">
  <!-- Sidebar -->
  <div class="w-64 h-screen bg-gray-200 p-4">
    <!-- Buttons at the top -->
    <div class="flex flex-col">
      <!-- ... existing button code ... -->
    </div>

    <!-- Selected options at the bottom -->
    <div class="mt-auto">
      <h3 class="text-lg font-semibold">Selected Options:</h3>
      <p>Twin World: {$twdata.twin_world || 'Not selected'}</p>
      <p>Cost Model: {$twdata.cost_model || 'Not selected'}</p>
      <p>Algorithm: {$twdata.algorithm || 'Not selected'}</p>
    </div>
  </div>

  <!-- Main Content -->
  <div class="flex-1">
    <!-- Your existing content here -->
  </div>
</div>
