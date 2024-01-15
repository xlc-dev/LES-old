<script lang="ts">
  import { stepperData } from "./lib/stores";
  import { OpenAPI } from "./lib/client";

  import Stepper from "./components/stepper.svelte";
  import BaseLayout from "./components/baseLayout.svelte";

  OpenAPI.BASE = "http://localhost:8000";
</script>

{#if $stepperData.length !== 0}
  <BaseLayout />
{:else}
  <Stepper />
{/if}
