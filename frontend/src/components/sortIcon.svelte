<script>
  export let isSortedAsc = false;
  export let isSortedDesc = false;
  export let onSort;
</script>

<button class="inline-block cursor-pointer" on:click={onSort}>
  <svg class="w-2 h-2.5 {isSortedAsc ? 'text-les-sort-active' : 'text-les-sort-inactive'}" viewBox="0 0 24 24">
    <path id="Triangle-2" data-name="Triangle" d="M10.2,3.1l-8,16A2,2,0,0,0,4,22H20a2,2,0,0,0,1.8-2.9l-8-16A2,2,0,0,0,10.2,3.1Z" fill="currentColor" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
  </svg>
  <svg class="w-2 h-2.5 {isSortedDesc ? 'text-les-sort-active' : 'text-les-sort-inactive'}" viewBox="0 0 24 24">
    <path id="Triangle-2" data-name="Triangle" d="M10.2 20.9l-8-16A2 2 0 0 1 4 2H20a2 2 0 0 1 1.8 2.9l-8 16A2 2 0 0 1 10.2 20.9Z" fill="currentColor" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
  </svg>
</button>
