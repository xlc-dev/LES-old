<script lang="ts">
  import { onMount } from "svelte";
  import { stepperData, twdata } from "../lib/stores";

  import { SimulateService, type SimulationData } from "../lib/client";

  let currentStep: number = 1;

  let simulationData: SimulationData = {
    algorithm: [],
    twin_world: [],
    cost_model: [],
  };

  let selectedIDs = {
    twin_world: 0,
    cost_model: 0,
    algorithm: 0,
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
      // Check if any selectedID is still 0
      if (
        selectedIDs.algorithm === 0 ||
        selectedIDs.twin_world === 0 ||
        selectedIDs.cost_model === 0
      ) {
        return;
      }

      // If all IDs are non-zero, but we haven't reached the final step, don't proceed
      currentStep += 1;
      currentDescription = simulationData[keys[currentStep - 1]][0]?.description || "";
    } else {
      // If all IDs are non-zero at this stage, execute the API call
      if (
        selectedIDs.algorithm !== 0 &&
        selectedIDs.twin_world !== 0 &&
        selectedIDs.cost_model !== 0
      ) {
        await SimulateService.startApiSimulateStartPost({
          algorithm_id: selectedIDs.algorithm,
          twinworld_id: selectedIDs.twin_world,
          costmodel_id: selectedIDs.cost_model,
        }).then((res) => ($stepperData = res));
      }
    }
  };

  const prevStep = () => {
    const keys = Object.keys(simulationData) as (keyof SimulationData)[];
    if (currentStep > 1) {
      currentStep -= 1;
      currentDescription = simulationData[keys[currentStep - 1]][0]?.description || "";
    }
  };

  const selectOption = (optionId: number, category: any, optionName: string) => {
    selectedIDs[category] = optionId;
    twdata.update((data) => ({ ...data, [category]: optionName }));
    nextStep();
  };

  const isStepCompleted = (step: number): boolean => {
    const keys = Object.keys(selectedIDs) as (keyof typeof selectedIDs)[];
    const currentStepKey = keys[step - 1];
    return selectedIDs[currentStepKey] !== 0;
  };

  const goToStep = (stepNumber: number) => {
    currentStep = stepNumber;
    currentDescription = simulationData[Object.keys(simulationData)[currentStep - 1]][0]?.description || "";
  };
</script>

<div class="max-w-3xl mx-auto">
  <div class="flex items-center justify-between mt-8">
    {#key selectedIDs}
      {#each Object.keys(simulationData) as _, index}
        <div class="relative flex items-center">
          <button
            class={`h-8 w-8 flex items-center justify-center rounded-full border-2
              ${currentStep === index + 1 ? 'bg-les-red-dark border-les-red text-white' :
              (isStepCompleted(index + 1) ? 'bg-les-highlight border-blue-500 text-white' : 'border-gray-300 text-gray-400')}`}
            on:click={() => goToStep(index + 1)}>
            <span class="text-sm font-bold">
              {#if isStepCompleted(index + 1)}✔{:else}{index + 1}{/if}
            </span>
          </button>
          {#if index !== Object.keys(simulationData).length - 1}
            <div class="h-0.5 flex-grow bg-red-400 mx-2 self-center"></div>
          {/if}
        </div>
      {/each}
    {/key}
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
                  on:click={() => selectOption(option.id, key, option.name)}
                  on:focus={() => updateDescription(option.description)}
                  on:mouseover={() => updateDescription(option.description)}
                  class="cursor-pointer hover:text-les-highlight">
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
    <button class="mt-8 px-4 py-2 rounded-lg bg-les-highlight text-white border-blue-500 border-2" on:click={prevStep}
      >Back</button>
  {/if}
</div>
