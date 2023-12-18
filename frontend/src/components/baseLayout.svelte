<script lang="ts">
  import {stepperData, twdata} from "../lib/stores";
  import Sidebar from "../partials/Sidebar.svelte";
  import SchedulableLoadTable from "../partials/SchedulableLoadTable.svelte";

  console.log($stepperData);
</script>

<div class="flex">
  <Sidebar />
  <div class="flex-1 bg-les-frame">
    <SchedulableLoadTable />
  </div>
</div>
