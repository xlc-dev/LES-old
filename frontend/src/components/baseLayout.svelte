<script lang="ts">
  import {stepperData, twdata} from "../lib/stores";
  import Sidebar from "../partials/Sidebar.svelte";
  import SchedulableLoadTable from "../partials/SchedulableLoadTable.svelte";

  console.log($stepperData);
</script>
<!--&lt;!&ndash;      To view the ids of all the households in the current twin world:&ndash;&gt;-->
<!--      {#each $stepperData as data}-->
<!--        <p>{data.id}</p>-->
<!--      {/each}-->
<!--    </div>-->
<!--  </div>-->

<div class="flex">
  <Sidebar />
  <div class="flex-1 bg-les-frame">
    <SchedulableLoadTable />
  </div>
</div>
