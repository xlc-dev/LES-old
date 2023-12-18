<script lang="ts">
  import { onMount } from "svelte";
  import { fade } from "svelte/transition";
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

    if (currentStep === 3) {
      const skippedStep = Object.entries(selectedIDs).find(([_, value]) => value === 0);

      if (skippedStep) {
        const [skippedID] = skippedStep;
        const targetStep = keys.findIndex((key) => key === skippedID);

        if (targetStep !== -1) {
          currentStep = targetStep + 1;
          currentDescription = simulationData[skippedID][0]?.description || "";
          return; // Exit the function after skipping to the specific step
        }
      }
    }

    if (currentStep < keys.length) {
      currentStep += 1;
      currentDescription = simulationData[keys[currentStep - 1]][0]?.description || "";
    }
  };

  const startSimulation = async () => {
    await SimulateService.startApiSimulateStartPost({
      algorithm_id: selectedIDs.algorithm,
      twinworld_id: selectedIDs.twin_world,
      costmodel_id: selectedIDs.cost_model,
    }).then((res) => ($stepperData = res));
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
    currentDescription =
      simulationData[Object.keys(simulationData)[currentStep - 1]][0]?.description || "";
  };
</script>

<div class="max-w-3xl mx-auto">
  <div class="flex items-center justify-between mt-16">
    {#key selectedIDs}
      {#each Object.keys(simulationData) as stepName, index}
        <div class="relative flex items-center">
          <button
            class={`h-8 w-8 flex items-center justify-center rounded-full border-2
            ${
              currentStep === index + 1
                ? "bg-les-red-dark border-les-red text-white"
                : isStepCompleted(index + 1)
                  ? "bg-les-highlight border-les-blue hover:bg-les-blue text-white transition-colors duration-200"
                  : "border-gray-300 text-gray-400 hover:bg-les-blue transition-colors duration-200"
            }`}
            on:click={() => goToStep(index + 1)}>
            <span class="text-sm font-bold">
              {#if isStepCompleted(index + 1)}✔{:else}{index + 1}{/if}
            </span>
            <span class="absolute bottom-10 text-xs font-semibold">
              {stepName.charAt(0).toUpperCase() + stepName.slice(1).replace("_", " ")}
            </span>
          </button>
          {#if index < Object.keys(simulationData).length - 1}
            <div
              class={`absolute top-4 left-8 border-t-2 w-[21rem] transition-colors duration-200 ${
                isStepCompleted(index + 1) ? "border-les-blue" : "border-gray-300"
              }`}>
            </div>
          {/if}
        </div>
      {/each}
    {/key}
  </div>

  {#each Object.keys(simulationData) as key, index}
    {#if currentStep === index + 1}
      <div class="mt-8 bg-white rounded-lg p-4 min-h-[20em]">
        <h2 class="text-3xl font-semibold text-center">
          {key.charAt(0).toUpperCase() + key.slice(1).replace("_", " ")}
        </h2>
        <div class="flex space-x-4 mt-4" in:fade>
          <div class="w-1/2">
            <h2 class="font-bold text-lg">Option:</h2>
            <div class="border p-4">
              <ul class="flex flex-col gap-4 items-start">
                {#each simulationData[key] as option (option.id)}
                  <button
                    on:click={() => selectOption(option.id, key, option.name)}
                    on:focus={() => updateDescription(option.description)}
                    on:mouseover={() => updateDescription(option.description)}
                    class="cursor-pointer hover:text-les-blue">
                    {option.name}
                  </button>
                {/each}
              </ul>
            </div>
          </div>
          <div class="w-1/2">
            <h2 class="font-bold text-lg">Description:</h2>
            <div class="border p-4">
              <p>{currentDescription}</p>
            </div>
          </div>
        </div>
      </div>
    {/if}
  {/each}
  <div class="flex justify-between mt-8">
    {#if currentStep !== 1}
      <button
        class="px-4 py-2 rounded-lg bg-les-highlight text-white border-les-blue border-2 hover:bg-les-blue transition-colors duration-200"
        on:click={prevStep}>Back</button>
    {/if}
    {#if selectedIDs.algorithm !== 0 && selectedIDs.twin_world !== 0 && selectedIDs.cost_model !== 0}
      <button
        class="px-4 py-2 rounded-lg bg-les-highlight text-white border-les-red border-2 hover:bg-les-red transition-colors duration-200"
        on:click={startSimulation}>Start</button>
    {/if}
  </div>
  <div class="mt-8">
    <p class="font-bold text-lg text-white mb-4">Selected:</p>
    <p class="text-white">
      {#if selectedIDs.twin_world !== 0}
        Twin World: {$twdata.twin_world}
      {:else}
        Twin World: -
      {/if}
      {#if selectedIDs.cost_model !== 0}
        <br />Cost Model: {$twdata.cost_model}
      {:else}
        <br />Cost Model: -
      {/if}
      {#if selectedIDs.algorithm !== 0}
        <br />Algorithm: {$twdata.algorithm}
      {:else}
        <br />Algorithm: -
      {/if}
    </p>
  </div>
</div>
