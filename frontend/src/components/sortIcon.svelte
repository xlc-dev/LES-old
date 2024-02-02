<script lang="ts">
  /**
   * The sortIcon component contains the SVG paths of the specific shapes that are used for the
   * sorting buttons in the filter bars of the schedulable load table and the simulation view.
   */

  export let isSortedAsc = false;
  export let isSortedDesc = false;
  export let onSort: () => void;
</script>

<button class="relative inline-block cursor-pointer" on:click={onSort}>
  <div class="absolute -translate-y-4 transform">
    <svg
      class="w-2 h-2.5 {isSortedAsc ? 'text-les-gray-400' : 'text-les-gray-300'}"
      viewBox="0 0 24 24">
      <path
        id="Triangle-2"
        data-name="Triangle"
        d="M10.2,3.1l-8,16A2,2,0,0,0,4,22H20a2,2,0,0,0,1.8-2.9l-8-16A2,2,0,0,0,10.2,3.1Z"
        fill="currentColor"
        stroke="currentColor"
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2" />
    </svg>

    <svg
      class="w-2 h-2.5 {isSortedDesc ? 'text-les-gray-400' : 'text-les-gray-300'}"
      viewBox="0 0 24 24">
      <path
        id="Triangle-2"
        data-name="Triangle"
        d="M10.2 20.9l-8-16A2 2 0 0 1 4 2H20a2 2 0 0 1 1.8 2.9l-8 16A2 2 0 0 1 10.2 20.9Z"
        fill="currentColor"
        stroke="currentColor"
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2" />
    </svg>
  </div>
</button>
