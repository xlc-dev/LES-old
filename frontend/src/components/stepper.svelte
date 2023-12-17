<script lang="ts">
  import { onMount } from "svelte";
  import { stepperData } from "../lib/stores";

  import { SimulateService, type SimulationData } from "../lib/client";

  let currentStep: number = 1;

  let simulationData: SimulationData = {
    algorithm: [],
    twin_world: [],
    cost_model: [],
  };

  let selectedIDs = {
    twin_world: 0,
    algorithm: 0,
    cost_model: 0,
  };

  let currentDescription: string = "";

  const updateDescription = (description: string) => {
    currentDescription = description;
  };

  onMount(async () => {
    const data: SimulationData = await SimulateService.getDataApiSimulateLoadDataGet();
    simulationData = data;

    const keys = Object.keys(simulationData) as (keyof SimulationData)[];
    currentDescription = simulationData[keys[currentStep - 1]][0]?.description || "";
  });

  const nextStep = async () => {
    const keys = Object.keys(simulationData) as (keyof SimulationData)[];
    if (currentStep < keys.length) {
      currentStep += 1;
      currentDescription = simulationData[keys[currentStep - 1]][0]?.description || "";
    } else {
      if (
        selectedIDs.algorithm === 0 ||
        selectedIDs.twin_world === 0 ||
        selectedIDs.cost_model === 0
      ) {
        alert("Please select all options");
        return;
      }

      await SimulateService.startApiSimulateStartPost({
        algorithm_id: selectedIDs.algorithm,
        twinworld_id: selectedIDs.twin_world,
        costmodel_id: selectedIDs.cost_model,
      }).then((res) => ($stepperData = res));
    }
  };

  const prevStep = () => {
    const keys = Object.keys(simulationData) as (keyof SimulationData)[];
    if (currentStep > 1) {
      currentStep -= 1;
      currentDescription = simulationData[keys[currentStep - 1]][0]?.description || "";
    }
  };

  const selectOption = (optionId: any, category: any) => {
    selectedIDs[category] = optionId;
    nextStep();
  };
</script>

<div class="max-w-3xl mx-auto">
  <div class="bg-gray-200 h-4 rounded-full mt-8">
    <div
      class="bg-blue-500 h-full rounded-full duration-300 ease-in-out transition-width"
      style={`width: ${(currentStep - 1) * 50}%`}>
    </div>
  </div>

  {#each Object.keys(simulationData) as key, index}
    {#if currentStep === index + 1}
      <div class="mt-8 bg-white rounded-lg p-4">
        <h2 class="text-3xl font-semibold text-center">
          {#if currentStep === 1}
            Twin World
          {:else if currentStep === 2}
            Cost Model
          {:else}
            Algorithm
          {/if}
        </h2>
        <div class="flex space-x-4 mt-4">
          <div class="w-1/2 border p-4">
            <ul class="flex flex-col gap-4 items-start">
              {#each simulationData[key] as option (option.id)}
                <button
                  on:click={() => selectOption(option.id, key)}
                  on:focus={() => updateDescription(option.description)}
                  on:mouseover={() => updateDescription(option.description)}
                  class="cursor-pointer hover:text-blue-500">
                  {option.name}
                </button>
              {/each}
            </ul>
          </div>
          <div class="w-1/2 border p-4">
            <p>{currentDescription}</p>
          </div>
        </div>
      </div>
    {/if}
  {/each}
  {#if currentStep !== 1}
    <button class="mt-8 px-4 py-2 rounded-lg bg-blue-500 text-white" on:click={prevStep}
      >Back</button>
  {/if}
</div>
