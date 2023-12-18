<script lang="ts">
  import Sidebar from "./sidebar.svelte";
  import SchedulableLoadTable from "./schedulableLoadTable.svelte";
</script>

<div class="flex">
  <Sidebar />
  <div class="flex-1 bg-les-frame">
    <SchedulableLoadTable />
  </div>
</div>
