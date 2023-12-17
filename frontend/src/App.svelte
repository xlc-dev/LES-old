<script lang="ts">
  import Stepper from "./components/stepper.svelte";
  import BaseLayout from "./components/baseLayout.svelte";

  import { stepperData } from "./lib/stores";

  import { OpenAPI } from "./lib/client";

  OpenAPI.BASE = "http://localhost:8000";
</script>

<main>
  {#if $stepperData.length !== 0}
    <BaseLayout />
  {:else}
    <Stepper />
  {/if}
</main>
