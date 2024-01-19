<script lang="ts">
  import { stepperData } from "./lib/stores";
  import { OpenAPI, SimulateService } from "./lib/client";

  import Stepper from "./components/stepper.svelte";
  import BaseLayout from "./components/baseLayout.svelte";

  OpenAPI.BASE = "http://localhost:8000";

  const call = SimulateService.planApiSimulatePlanPost({
    chunkoffset: 0, // constantly increase with 7 when recursion occurs
    costmodel: $stepperData.costmodel,
    algorithm: $stepperData.algorithm,
    twinworld: $stepperData.twinworld,
    households: $stepperData.households,
  }).then((res) => {
    // update other store(s) with results for dashboard
    // timedaily store (cumulative, not replacing)

    // call the function again (recursion): chunkoffset + 7

  }).catch((err) => {
    // catch and show
    // if the error code is not 500, call the function again (recursion)
  })
    // else load result component (can also be done in the if else statement below)
 </script>

{#if $stepperData.households.length !== 0}
  <BaseLayout />
{:else}
  <Stepper />
{/if}
