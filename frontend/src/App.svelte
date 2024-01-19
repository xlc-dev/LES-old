<script lang="ts">
  import { stepperData } from "./lib/stores";
  import { OpenAPI, SimulateService } from "./lib/client";

  import Stepper from "./components/stepper.svelte";
  import BaseLayout from "./components/baseLayout.svelte";

  OpenAPI.BASE = "http://localhost:8000";

  const call = SimulateService.planApiSimulatePlanPost({
    chunkoffset: 0, // telkens ophogen met 7 bij recursie
    costmodel: $stepperData.costmodel,
    algorithm: $stepperData.algorithm,
    twinworld: $stepperData.twinworld,
    households: $stepperData.households,
  }).then((res) => {
    // andere store updaten met de results voor dashboard
    // timedaily store (cumulatief, niet vervangend)

    // call again: chunkoffset + 7

  }).catch((err) => {
    // afvangen en laten zien. opnieuw proberen als het kan (geen 500)
    // als andere error dan 500, pas recursie toe
  })
    //else end view
 </script>

{#if $stepperData.households.length !== 0}
  <BaseLayout />
{:else}
  <Stepper />
{/if}
