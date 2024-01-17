<script lang="ts">
  import { onMount } from "svelte";
  import { fade } from "svelte/transition";

  import * as monaco from "monaco-editor";

  import { stepperData, twdata } from "../lib/stores";

  import {
    SimulateService,
    type SimulationData,
    TwinWorldService,
    CostModelService,
    AlgorithmService,
    HouseholdService,
    type ApplianceCreate,
    type HouseholdCreate,
    ApplianceType,
    ApplianceService,
    type HouseholdRead_Output,
    type ApplianceRead_Output,
    type ApplianceTimeWindowCreate,
    ApplianceDays,
    type ApplianceTimeWindowRead,
  } from "../lib/client";

  let hoursArray = [
    "00:00",
    "01:00",
    "02:00",
    "03:00",
    "04:00",
    "05:00",
    "06:00",
    "07:00",
    "08:00",
    "09:00",
    "10:00",
    "11:00",
    "12:00",
    "13:00",
    "14:00",
    "15:00",
    "16:00",
    "17:00",
    "18:00",
    "19:00",
    "20:00",
    "21:00",
    "22:00",
    "23:00",
  ];

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

  let newHousehold: HouseholdCreate = {
    name: "",
    size: 1,
    energy_usage: 0,
    solar_panels: 0,
    solar_yield_yearly: 0,
    twinworld_id: 0,
  };

  let newAppliance: ApplianceCreate = {
    name: ApplianceType.STOVE,
    power: 0,
    duration: 0,
    daily_usage: 0,
    household_id: 0,
  };

  let newTimeWindow: ApplianceTimeWindowCreate = {
    day: ApplianceDays.MONDAY,
    bitmap_window: 0,
    appliance_id: 0,
  };

  let costmodelEditor: monaco.editor.IStandaloneCodeEditor;
  let algorithmEditor: monaco.editor.IStandaloneCodeEditor;
  let costmodelCode = "";
  let algorithmCode = "import pandas\nimport numpy\nimport scipy\nimport math\nimport random\n\ndef run():\n    pass\n";

  let checkboxStates = Array(24).fill(false);
  let currentStep: number = 1;

  let currentDescription: string = "";
  let currentAppliances: ApplianceRead_Output[] = null;

  let applianceToAdd: number = 0;
  let timewindowToAdd: number = 0;

  let twinWorlds = [];
  let twinworldHouseholds = [];

  let householdError: string = "";
  let applianceError: string = "";
  let timewindowError: string = "";
  let algorithmError: string = "";

  let applianceCheck: Array<{
    householdName: string;
    appliance: string;
    missingDay: ApplianceDays;
  }> = [];

  let editingHousehold: HouseholdRead_Output = null;
  let editingApplianceTimeWindow: ApplianceTimeWindowRead = null;

  const updateDescription = (description: string) => {
    currentDescription = description;
  };

  const startEditingHousehold = (household: HouseholdRead_Output) => {
    editingHousehold = household;
  };

  const startEditingTimewindow = (timewindow: ApplianceTimeWindowRead) => {
    editingApplianceTimeWindow = timewindow;
  };

  const scrollToApplianceLocation = () => {
    const applianceLocation = document.getElementById("applianceLocation");
    if (applianceLocation) {
      applianceLocation.scrollIntoView({ behavior: "smooth" });
    }
  };

  const scrollToTimewindowLocation = () => {
    const applianceLocation = document.getElementById("timewindowLocation");
    if (applianceLocation) {
      applianceLocation.scrollIntoView({ behavior: "smooth" });
    }
  };

  const updateBitmapWindow = () => {
    newTimeWindow.bitmap_window = checkboxStates.reduce((acc, state: any, index) => {
      return acc | (state << index);
    }, 0);
  };

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
          return;
        }
      }
    }

    if (currentStep < keys.length) {
      currentStep += 1;
      currentDescription = simulationData[keys[currentStep - 1]][0]?.description || "";
    }
  };

  const prevStep = () => {
    const keys = Object.keys(simulationData) as (keyof SimulationData)[];
    if (currentStep > 1) {
      currentStep -= 1;
      currentDescription = simulationData[keys[currentStep - 1]][0]?.description || "";
    }
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

  const selectOption = (optionId: number, category: any, optionName: string) => {
    selectedIDs[category] = optionId;
    twdata.update((data) => ({ ...data, [category]: optionName }));
  };

  const deleteOption = async (optionId: number, category: any) => {
    selectedIDs[category] = 0;
    twdata.update((data) => ({ ...data, [category]: "-" }));
    await deleteOptionBasedOnCategory(category, optionId);
    simulationData = await SimulateService.getDataApiSimulateLoadDataGet();
  };

  const deleteOptionBasedOnCategory = async (category: keyof SimulationData, optionId: number) => {
    switch (category) {
      case "cost_model":
        await CostModelService.deleteCostmodelApiCostmodelIdDelete(optionId);
        break;
      case "twin_world":
        await TwinWorldService.deleteTwinworldApiTwinworldIdDelete(optionId);
        break;
      case "algorithm":
        await AlgorithmService.deleteAlgorithmApiAlgorithmIdDelete(optionId);
        break;
      default:
        break;
    }
  };

  const initMonaco = (node: HTMLElement, { initialCode, onChange }) => {
    const editor = monaco.editor.create(node, {
      value: initialCode,
      language: "python",
      lineNumbers: "on",
      automaticLayout: true,
    });

    const handleEditorChange = () => {
      const newValue = editor.getValue();
      if (validatePythonSyntax(newValue)) {
        onChange(newValue);
        monaco.editor.setModelMarkers(editor.getModel(), "python", []);
      } else {
        monaco.editor.setModelMarkers(editor.getModel(), "python", [
          {
            startLineNumber: 1,
            startColumn: 1,
            endLineNumber: 1,
            endColumn: 1,
            message: "Code is not valid Python syntax",
            severity: monaco.MarkerSeverity.Error,
          },
        ]);
      }
    };

    editor.onDidChangeModelContent(handleEditorChange);

    return {
      update({ initialCode }) {
        if (initialCode !== editor.getValue()) {
          editor.setValue(initialCode);
        }
      },
      destroy() {
        editor.dispose();
      },
    };
  };

  const validatePythonSyntax = (code: string) => {
    const pythonPattern =
      /(?:def|class)\s+\w+\s*\(.*\)\s*:\s*|import\s+\w+|from\s+\w+\s+import\s+\w+/;
    return pythonPattern.test(code);
  };

  const addTimewindow = async () => {
    if (checkboxStates.every((state) => state === false)) {
      timewindowError = "Please select at least one hour";
      return;
    }

    if (newTimeWindow.appliance_id === 0) {
      timewindowError = "Please select at least one appliance";
      return;
    }

    await ApplianceService.postApplianceTimewindowApiApplianceTimewindowPost(newTimeWindow)
      .then(async () => {
        twinworldHouseholds =
          await HouseholdService.getHouseholdsByTwinworldApiHouseholdTwinworldTwinworldIdGet(
            selectedIDs.twin_world
          );

        checkboxStates = Array(24).fill(false);
        timewindowError = "";
      })
      .catch((err) => {
        timewindowError = err.message;
      });
  };

  const deleteTimewindow = async (id: number) => {
    try {
      await ApplianceService.deleteApplianceTimewindowApiAppliancetimewindowIdDelete(id);
      twinworldHouseholds = twinworldHouseholds.map((household) => {
        household.appliances = household.appliances.map((appliance: ApplianceRead_Output) => {
          // Check if the current appliance has an appliance_windows array
          if (appliance.appliance_windows) {
            // Filter out the specific appliance_time_window based on its ID
            appliance.appliance_windows = appliance.appliance_windows.filter(
              (window) => window.id !== id
            );
          }
          return appliance;
        });
        return household;
      });
    } catch (err) {
      console.log(err);
    }
  };

  const stopEditingTimewindow = async () => {
    try {
      await ApplianceService.updateApplianceTimewindowApiApplianceTimewindowIdPatch(
        editingApplianceTimeWindow.id,
        editingApplianceTimeWindow
      );
      editingApplianceTimeWindow = null;
    } catch (err) {
      console.log(err);
    }
  };

  const addAppliance = async () => {
    newAppliance.household_id = applianceToAdd;
    await ApplianceService.postApplianceApiAppliancePost(newAppliance)
      .then(async () => {
        twinworldHouseholds =
          await HouseholdService.getHouseholdsByTwinworldApiHouseholdTwinworldTwinworldIdGet(
            selectedIDs.twin_world
          );

        applianceToAdd = 0;
        applianceError = "";
      })
      .catch((err) => {
        applianceError = err.message;
      });
  };

  const deleteAppliance = async (id: number) => {
    try {
      await ApplianceService.deleteApplianceApiApplianceIdDelete(id);

      twinworldHouseholds = twinworldHouseholds.map((household) => {
        household.appliances = household.appliances.filter(
          (appliance: ApplianceRead_Output) => appliance.id !== id
        );
        return household; // return so svelte can update the array
      });
    } catch (err) {
      console.log(err);
    }
  };

  const addHousehold = async () => {
    newHousehold.twinworld_id = selectedIDs.twin_world;
    await HouseholdService.postHouseholdApiHouseholdPost(newHousehold)
      .then(async () => {
        twinworldHouseholds =
          await HouseholdService.getHouseholdsByTwinworldApiHouseholdTwinworldTwinworldIdGet(
            selectedIDs.twin_world
          );
        applianceToAdd = 0;
        householdError = "";
      })
      .catch((err) => {
        householdError = err.message;
      });
  };

  const deleteHousehold = async (id: number) => {
    await HouseholdService.deleteHouseholdApiHouseholdIdDelete(id)
      .then(() => {
        twinworldHouseholds = twinworldHouseholds.filter((household) => household.id !== id);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const stopEditingHousehold = async () => {
    try {
      await HouseholdService.updateHouseholdApiHouseholdIdPatch(
        editingHousehold.id,
        editingHousehold
      );
      editingHousehold = null;
    } catch (err) {
      console.log(err);
    }
  };

  const fetchHouseholds = async () => {
    twinworldHouseholds =
      await HouseholdService.getHouseholdsByTwinworldApiHouseholdTwinworldTwinworldIdGet(
        selectedIDs.twin_world
      );
  };

  const uploadCostModel = async (event: any) => {
    const target = event.target;

    const formData = {
      name: target.name.value,
      description: target.description.value,
      price_network_buy_consumer: target.price_network_buy_consumer.value,
      price_network_sell_consumer: target.price_network_sell_consumer.value,
      fixed_price_ratio: target.fixed_price_ratio.value,
      costmodel_algorithm: costmodelCode,
    };

    try {
      await CostModelService.postCostmodelApiCostmodelPost(formData);
      simulationData = await SimulateService.getDataApiSimulateLoadDataGet();
    } catch (error) {
      console.log(error);
    }
  };

  const uploadTwinWorld = async (event: any) => {
    const target = event.target;

    const formData = {
      name: target.name.value,
      description: target.description.value,
      households: twinworldHouseholds,
    };

    try {
      await TwinWorldService.postTwinworldApiTwinworldPost(formData);
      simulationData = await SimulateService.getDataApiSimulateLoadDataGet();
      twinworldHouseholds = [];
    } catch (error) {
      console.error(error);
    }
  };

  const uploadAlgorithm = async (event: any) => {
    const target = event.target;

    const formData = {
      name: target.name.value,
      description: target.description.value,
      algorithm: algorithmCode,
    };

    try {
      await AlgorithmService.postAlgorithmApiAlgorithmPost(formData);
      simulationData = await SimulateService.getDataApiSimulateLoadDataGet();
      algorithmError = "";
    } catch (err) {
      algorithmError = err.message;
    }
  };

  const startSimulation = async () => {
    applianceCheck = [];
    const hasApplianceWithoutEveryDay = twinworldHouseholds
      .map((household) =>
        household.appliances.map((appliance: ApplianceRead_Output) => {
          // Check if the current appliance has an appliance_windows array
          if (appliance.appliance_windows) {
            const missingDays = Object.values(ApplianceDays).filter(
              (day) => !appliance.appliance_windows.some((window) => window.day === day)
            );

            // If missingDays is not empty, add information to applianceCheck
            if (missingDays.length > 0) {
              missingDays.forEach((day) => {
                applianceCheck.push({
                  householdName: household.name,
                  appliance: appliance.name,
                  missingDay: day,
                });
              });
            }

            return missingDays.length > 0; // Return true if missingDays is not empty
          }

          return false; // Return false if appliance_windows is undefined or null
        })
      )
      .flat()
      .some(Boolean);

    if (hasApplianceWithoutEveryDay) {
      applianceCheck = applianceCheck;
      goToStep(1);
      return; // Don't continue with the function if an appliance doesn't have every day
    }

    await SimulateService.startApiSimulateStartPost({
      algorithm_id: selectedIDs.algorithm,
      twinworld_id: selectedIDs.twin_world,
      costmodel_id: selectedIDs.cost_model,
    }).then((res) => ($stepperData = res));
  };

  onMount(async () => {
    const data: SimulationData = await SimulateService.getDataApiSimulateLoadDataGet();
    simulationData = data;

    twinWorlds = await TwinWorldService.getTwinworldsApiTwinworldGet();

    const keys = Object.keys(simulationData) as (keyof SimulationData)[];
    currentDescription = simulationData[keys[currentStep - 1]][0]?.description || "";

    costmodelEditor = monaco.editor.create(document.getElementById("algo1-editor"), {
      value: "",
      language: "python",
      lineNumbers: "on",
      automaticLayout: true,
    });

    algorithmEditor = monaco.editor.create(document.getElementById("algo2-editor"), {
      value: "",
      language: "python",
      lineNumbers: "on",
      automaticLayout: true,
    });
  });

  $: selectedIDs.twin_world && fetchHouseholds();

  $: if (applianceToAdd > 0) {
    setTimeout(() => {
      scrollToApplianceLocation();
    }, 100);
  }

  $: if (timewindowToAdd > 0) {
    // Find the household with the matching id in twinworldHouseholds array
    const matchingHousehold = twinworldHouseholds.find(
      (household) => household.id === timewindowToAdd
    );

    if (matchingHousehold) {
      currentAppliances = matchingHousehold.appliances;
    }

    setTimeout(() => {
      scrollToTimewindowLocation();
    }, 100);
  }
</script>

<div class="max-w-3xl mx-auto pt-8">
  <h1 class="font-bold text-white text-4xl text-center">Local Energy System Simulation</h1>

  <p class="text-white text-xl text-center py-4">
    Welcome to the Local Energy System simulation. Explaination here.
  </p>

  {#if applianceCheck.length > 0}
    <div
      class="bg-les-white p-8 border-2 border-gray-400 rounded-lg flex flex-col justify-center items-center">
      <p class="text-xl font-bold text-les-highlight text-center w-full pb-4">
        Appliances to fix:
      </p>

      {#each applianceCheck as check}
        <p class="text-les-red">
          Household <strong>{check.householdName}</strong> is missing time window for
          <strong>{check.missingDay}</strong>
          in appliance <strong>{check.appliance}</strong>.
        </p>
      {/each}
    </div>
  {/if}

  <div class="flex items-center justify-between mt-16">
    {#key selectedIDs}
      {#each Object.keys(simulationData) as stepName, index}
        <div class="relative flex items-center pb-8">
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

            <span class="absolute bottom-20 text-xs font-semibold w-20">
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

          <p class="text-white absolute top-10 transform -translate-x-28 w-64 text-center">
            {#if selectedIDs.twin_world !== 0 && stepName === "twin_world"}
              {#if applianceCheck.length > 0}
                <span class="!text-les-red">{$twdata.twin_world}</span>
              {:else}
                {$twdata.twin_world}
              {/if}
            {:else if selectedIDs.cost_model !== 0 && stepName === "cost_model"}
              {$twdata.cost_model}
            {:else if selectedIDs.algorithm !== 0 && stepName === "algorithm"}
              {$twdata.algorithm}
            {:else}
              -
            {/if}
          </p>
        </div>
      {/each}
    {/key}
  </div>

  {#each Object.keys(simulationData) as key, index}
    {#if currentStep === index + 1}
      <div class="mt-8 bg-white rounded-lg p-4 min-h-[20em] border-4 border-gray-400 shadow">
        <h2 class="text-3xl font-semibold text-center">
          {key.charAt(0).toUpperCase() + key.slice(1).replace("_", " ")}
        </h2>

        <div class="flex space-x-4 mt-4" in:fade>
          <div class="w-1/2">
            <h2 class="font-bold text-lg">Option:</h2>

            <div class="border p-4">
              <ul class="flex flex-col gap-4 items-start">
                {#each simulationData[key] as option (option.id)}
                  <div class="flex gap-2 items-center">
                    <button
                      on:click={() => selectOption(option.id, key, option.name)}
                      on:focus={() => updateDescription(option.description)}
                      on:mouseover={() => updateDescription(option.description)}
                      class="cursor-pointer hover:text-les-blue relative flex gap-2 items-center transition-colors duration-200"
                      class:text-les-blue={selectedIDs[key] === option.id}>
                      {option.name}
                    </button>

                    {#if option.id !== 1 && option.id !== 2}
                      <button on:click={() => deleteOption(option.id, key)}>
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke-width="1.5"
                          stroke="currentColor"
                          data-slot="icon"
                          class="stroke-les-red hover:stroke-les-red-dark h-4 cursor-pointer">
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                        </svg>
                      </button>
                    {/if}
                  </div>
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
        <div class="flex justify-between mt-8">
          {#if currentStep !== 1}
            <button
              class="px-6 py-3 rounded-lg text-white transition-colors duration-200 bg-les-highlight hover:bg-dark-les-bg"
              on:click={prevStep}>Back</button>
          {/if}

          {#if currentStep !== 3}
            <button
              class="px-6 py-3 rounded-lg text-white transition-colors duration-200 bg-les-blue hover:brightness-110"
              on:click={nextStep}>Next</button>
          {/if}

          {#if selectedIDs.algorithm !== 0 && selectedIDs.twin_world !== 0 && selectedIDs.cost_model !== 0}
            <button
              class="px-6 py-3 rounded-lg text-white transition-colors duration-200 bg-les-red hover:brightness-110"
              on:click={startSimulation}>Start</button>
          {/if}
        </div>
      </div>
    {/if}
  {/each}

  <div class="mt-8 bg-white rounded-lg p-4 mb-8 border-4 border-gray-400 shadow">
    <p class="font-bold text-lg mb-4">
      Upload Custom {Object.keys(simulationData)[currentStep - 1].charAt(0).toUpperCase() +
        Object.keys(simulationData)[currentStep - 1].slice(1).replace("_", " ")}:
    </p>

    {#if currentStep === 1}
      <form method="post" on:submit|preventDefault={uploadTwinWorld} class="flex flex-col gap-6">
        <label for="name" class="font-bold pt-4">Name:</label>
        <input
          type="text"
          name="name"
          class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
          required />

        <label for="description" class="font-bold">Description:</label>
        <textarea
          name="description"
          class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
          required></textarea>

        <button
          type="submit"
          class="py-3 bg-dark-les-bg rounded-lg text-white hover:bg-les-highlight transition-colors duration-200"
          >Submit</button>
      </form>

      {#if selectedIDs.twin_world}
        <hr class="my-8 bg-les-highlight" />

        <h2 class="font-bold text-lg mb-4">
          Add household for Twin World id: {selectedIDs.twin_world}
        </h2>

        <div class="flex flex-wrap">
          <div class="flex flex-col w-full sm:w-1/2 md:w-1/3 pr-4">
            <label for="name" class="font-bold">Name:</label>
            <input
              id="name"
              class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
              type="text"
              minlength="1"
              required
              bind:value={newHousehold.name}
              placeholder="Name" />
          </div>

          <div class="flex flex-col w-full sm:w-1/2 md:w-1/3 pr-4">
            <label for="size" class="font-bold">Size:</label>
            <input
              id="size"
              min="1"
              max="5"
              class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
              type="number"
              bind:value={newHousehold.size}
              placeholder="Size" />
          </div>

          <div class="flex flex-col w-full sm:w-1/2 md:w-1/3 pr-4">
            <label for="energy_usage" class="font-bold">Energy Usage:</label>
            <input
              id="energy_usage"
              class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
              type="number"
              min="0"
              bind:value={newHousehold.energy_usage}
              placeholder="Energy usage" />
          </div>

          <div class="flex flex-col w-full sm:w-1/2 md:w-1/3 pr-4">
            <label for="solar_panels" class="font-bold">Solar Panels:</label>
            <input
              id="solar_panels"
              class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
              type="number"
              min="0"
              bind:value={newHousehold.solar_panels}
              placeholder="Solar panels" />
          </div>

          <div class="flex flex-col w-full sm:w-1/2 md:w-1/3 pr-4">
            <label for="solar_yield_yearly" class="font-bold">Solar Yield Yearly:</label>
            <input
              id="solar_yield_yearly"
              class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
              type="number"
              min="0"
              bind:value={newHousehold.solar_yield_yearly}
              placeholder="Solar yield yearly" />
          </div>
          <div class="flex items-end">
            <button
              type="button"
              class="py-3 px-4 bg-dark-les-bg rounded-lg text-white hover:bg-les-highlight transition-colors duration-200"
              on:click={addHousehold}>Add Household</button>
          </div>

          {#if householdError}
            <p class="text-les-red">{householdError}</p>
          {/if}
        </div>

        {#if applianceToAdd > 0}
          <hr class="my-8 bg-les-highlight" id="applianceLocation" />

          <h2 class="text-lg font-bold pb-4">
            Add appliance for household id: {applianceToAdd}
          </h2>

          <div class="flex flex-wrap">
            <div class="flex flex-col w-full sm:w-1/2 md:w-1/3 pr-4">
              <label for="name" class="font-bold">Name:</label>
              <select
                id="type"
                class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
                bind:value={newAppliance.name}>
                {#each Object.values(ApplianceType) as type (type)}
                  <option value={type}>{type}</option>
                {/each}
              </select>
            </div>

            <div class="flex flex-col w-full sm:w-1/2 md:w-1/3 pr-4">
              <label for="power" class="font-bold">Power:</label>
              <input
                id="power"
                class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
                type="number"
                bind:value={newAppliance.power} />
            </div>

            <div class="flex flex-col w-full sm:w-1/2 md:w-1/3 pr-4">
              <label for="duration" class="font-bold">Duration:</label>
              <input
                id="duration"
                class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
                type="number"
                bind:value={newAppliance.duration} />
            </div>

            <div class="flex flex-col w-full sm:w-1/2 md:w-1/3 pr-4">
              <label for="daily_usage" class="font-bold">Daily Usage:</label>
              <input
                id="daily_usage"
                class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
                type="number"
                bind:value={newAppliance.daily_usage} />
            </div>

            <div class="flex items-end">
              <button
                type="button"
                class="py-3 px-4 bg-dark-les-bg rounded-lg text-white hover:bg-les-highlight transition-colors duration-200"
                on:click={addAppliance}>Add Appliance</button>
            </div>

            {#if applianceError}
              <p class="text-les-red">{applianceError}</p>
            {/if}
          </div>
        {/if}

        {#if timewindowToAdd > 0}
          <span id="timewindowLocation"></span>

          {#each currentAppliances as appliance}
            <hr class="my-8 bg-les-highlight" />
            <h3 class="font-bold text-lg">Timewindows for: {appliance.name}</h3>
            <table class="min-w-full leading-normal rounded-lg mt-4 overflow-hidden">
              {#if currentAppliances.length === 0}
                <p class="text-center text-gray-500 py-4">No timewindows added yet.</p>
              {:else}
                <thead>
                  <tr>
                    <th
                      class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs text-gray-600 uppercase tracking-wider"
                      >Day</th>
                    <th
                      class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs text-gray-600 uppercase tracking-wider"
                      >Bitmap Window</th>
                    <th
                      class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs text-gray-600 uppercase tracking-wider"
                      >Options</th>
                  </tr>
                </thead>
                <tbody>
                  {#each appliance.appliance_windows as appliance_window}
                    <tr class="bg-white text-sm hover:bg-gray-200">
                      <td class="px-5 py-5 border-b border-gray-200">
                        {#if editingApplianceTimeWindow === appliance_window}
                          <select
                            id="day"
                            class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
                            bind:value={appliance_window.day}>
                            {#each Object.values(ApplianceDays) as type (type)}
                              <option value={type}>{type}</option>
                            {/each}
                          </select>
                        {:else}
                          {appliance_window.day}
                        {/if}
                      </td>

                      <td class="px-5 py-5 border-b border-gray-200">
                        {#if editingApplianceTimeWindow === appliance_window}
                          <input
                            bind:value={appliance_window.bitmap_window}
                            class="border rounded-md px-2 py-1"
                            style="max-width: 130px;" />
                        {:else}
                          {appliance_window.bitmap_window}
                        {/if}
                      </td>

                      <td class="px-5 py-5 border-b border-gray-200 space-y-4">
                        {#if editingApplianceTimeWindow === appliance_window}
                          <button
                            type="button"
                            class="py-2 px-4 bg-dark-les-bg rounded-lg text-white hover:bg-les-green transition-colors duration-200"
                            on:click={stopEditingTimewindow}>
                            Done
                          </button>
                        {:else}
                          <button
                            type="button"
                            class="py-2 px-4 bg-dark-les-bg rounded-lg text-white hover:bg-les-blue transition-colors duration-200"
                            on:click={() => startEditingTimewindow(appliance_window)}>
                            <img src="/edit.svg" alt="" class="w-4 h-4" />
                          </button>

                          <button
                            type="button"
                            class="py-2 px-4 bg-dark-les-bg rounded-lg text-white hover:bg-les-red transition-colors duration-200"
                            on:click={() => deleteTimewindow(appliance_window.id)}>
                            <img src="/trash.svg" alt="" class="w-4 h-4" />
                          </button>
                        {/if}
                      </td>
                    </tr>
                  {/each}
                </tbody>
              {/if}
            </table>
          {/each}
          <hr class="my-8 bg-les-highlight" id="applianceLocation" />

          <h2 class="text-lg font-bold pb-4">
            Add timewindow for household id: {timewindowToAdd}
          </h2>

          <div class="flex flex-wrap">
            <div class="flex flex-col w-full sm:w-1/2 md:w-1/3 pr-4">
              <label for="day" class="font-bold">Day:</label>
              <select
                id="day"
                class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
                bind:value={newTimeWindow.day}>
                {#each Object.values(ApplianceDays) as type (type)}
                  <option value={type}>{type}</option>
                {/each}
              </select>
            </div>

            <div class="flex flex-col w-full sm:w-1/2 md:w-1/3 pr-4">
              <label for="appliance_id" class="font-bold">Appliance</label>
              <select
                id="appliance_id"
                class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
                bind:value={newTimeWindow.appliance_id}>
                {#each currentAppliances as appliance (appliance.id)}
                  <option value={appliance.id}>{appliance.name}</option>
                {/each}
              </select>
            </div>

            <div class="flex flex-col w-full sm:w-1/2 md:w-1/3 pr-4">
              <label for="bitmap_window_display" class="font-bold">Bitmap Window Value:</label>
              <input
                id="bitmap_window_display"
                class="bg-gray-300 cursor-not-allowed p-2.5 rounded-lg border-2 border-gray-400"
                type="text"
                readonly
                disabled
                value={newTimeWindow.bitmap_window} />
            </div>

            <div class="flex flex-col w-full sm:w-1/2 md:w-1/3 pr-4 pt-2">
              <label for="bitmap_window" class="font-bold">Bitmap Window:</label>
              <div class="flex flex-wrap">
                {#each hoursArray as hour, hourIndex}
                  <div class="flex items-center w-1/3 pr-4">
                    <input
                      id="bitmap_window_{hourIndex}"
                      class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
                      type="checkbox"
                      bind:checked={checkboxStates[hourIndex]}
                      on:change={updateBitmapWindow} />
                    <label for="bitmap_window_{hourIndex}" class="ml-2">{hour}</label>
                  </div>
                {/each}
              </div>
            </div>

            <div class="flex h-fit pt-8">
              <button
                type="button"
                class="py-3 px-4 w-fit bg-dark-les-bg rounded-lg text-white hover:bg-les-highlight transition-colors duration-200"
                on:click={addTimewindow}>Add Timewindow</button>
            </div>

            {#if timewindowError}
              <p class="text-les-red flex items-center">{timewindowError}</p>
            {/if}
          </div>
        {/if}
        <table class="min-w-full leading-normal rounded-lg mt-4 overflow-hidden">
          {#if twinworldHouseholds.length === 0}
            <p class="text-center text-gray-500 py-4">No households added yet.</p>
          {:else}
            <thead>
              <tr>
                <th
                  class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs text-gray-600 uppercase tracking-wider"
                  >Name</th>

                <th
                  class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs text-gray-600 uppercase tracking-wider"
                  >Size</th>
                <th
                  class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs text-gray-600 uppercase tracking-wider"
                  >Energy Usage</th>

                <th
                  class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs text-gray-600 uppercase tracking-wider"
                  >Solar Yield Yearly</th>

                <th
                  class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs text-gray-600 uppercase tracking-wider"
                  >Appliances</th>

                <th
                  class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs text-gray-600 uppercase tracking-wider"
                  >Options</th>
              </tr>
            </thead>
            <tbody>
              {#each twinworldHouseholds as household}
                <tr class="bg-white text-sm hover:bg-gray-200">
                  <td class="px-5 py-5 border-b border-gray-200">
                    {#if editingHousehold === household}
                      <input
                        bind:value={household.name}
                        class="border rounded-md px-2 py-1"
                        minlength="1"
                        style="max-width: 130px;" />
                    {:else}
                      {household.name}
                    {/if}
                  </td>

                  <td class="px-5 py-5 border-b border-gray-200">
                    {#if editingHousehold === household}
                      <input
                        type="number"
                        bind:value={household.size}
                        min="1"
                        max="5"
                        class="border rounded-md px-2 py-1"
                        style="max-width: 50px;" />
                    {:else}
                      {household.size}
                    {/if}
                  </td>

                  <td class="px-5 py-5 border-b border-gray-200">
                    {#if editingHousehold === household}
                      <input
                        type="number"
                        min="0"
                        bind:value={household.energy_usage}
                        class="border rounded-md px-2 py-1"
                        style="max-width: 80px;" />
                    {:else}
                      {household.energy_usage}
                    {/if}
                  </td>

                  <td class="px-5 py-5 border-b border-gray-200">
                    {#if editingHousehold === household}
                      <input
                        type="number"
                        min="0"
                        bind:value={household.solar_yield_yearly}
                        class="border rounded-md px-2 py-1"
                        style="max-width: 80px;" />
                    {:else}
                      {household.solar_yield_yearly}
                    {/if}
                  </td>

                  <td class="px-5 py-5 border-b border-gray-200">
                    {#each household.appliances as appliance}
                      <div class="flex gap-2 justify-between items-center max-w-[25px]">
                        <p class="pb-2">{appliance.name}</p>

                        <button on:click={() => deleteAppliance(appliance.id)} class="pb-2">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke-width="1.5"
                            stroke="currentColor"
                            data-slot="icon"
                            class="stroke-les-red hover:stroke-les-red-dark h-4 cursor-pointer">
                            <path
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                          </svg>
                        </button>
                      </div>
                    {/each}
                  </td>

                  <td class="px-5 py-5 border-b border-gray-200 space-y-4">
                    {#if editingHousehold === household}
                      <button
                        type="button"
                        class="py-2 px-4 bg-dark-les-bg rounded-lg text-white hover:bg-les-green transition-colors duration-200"
                        on:click={stopEditingHousehold}>
                        Done
                      </button>
                    {:else}
                      <button
                        type="button"
                        class="py-2 px-4 bg-dark-les-bg rounded-lg text-white hover:bg-les-blue transition-colors duration-200"
                        on:click={() => startEditingHousehold(household)}>
                        <img src="/edit.svg" alt="" class="w-4 h-4" />
                      </button>

                      <button
                        type="button"
                        class="py-2 px-4 bg-dark-les-bg rounded-lg text-white hover:bg-les-red transition-colors duration-200"
                        on:click={() => deleteHousehold(household.id)}>
                        <img src="/trash.svg" alt="" class="w-4 h-4" />
                      </button>

                      <button
                        type="button"
                        class="py-2 px-4 bg-dark-les-bg rounded-lg text-white hover:bg-les-blue transition-colors duration-200"
                        on:click={() => (applianceToAdd = household.id)}>
                        <img src="/plus.svg" alt="" class="w-4 h-4" />
                      </button>

                      {#if household.appliances.length > 0}
                        <button
                          type="button"
                          class="py-2 px-4 bg-dark-les-bg rounded-lg text-white hover:bg-les-blue transition-colors duration-200"
                          on:click={() => (timewindowToAdd = household.id)}>
                          <img src="/clock.svg" alt="" class="w-4 h-4" />
                        </button>
                      {/if}
                    {/if}
                  </td>
                </tr>
              {/each}
            </tbody>
          {/if}
        </table>
      {/if}
    {:else if currentStep === 2}
      <form
        method="post"
        on:submit|preventDefault={uploadCostModel}
        class="flex flex-col space-y-3">

        <div>
          <label for="name" class="font-bold pt-4">Name:</label>
          <p class="text-sm text-gray-500">Name of the costmodel</p>
        </div>

        <input
          type="text"
          name="name"
          class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
          required />

        <div>
          <label for="description" class="font-bold">Description:</label>
          <p class="text-sm text-gray-500">Description of the costmodel</p>
        </div>

        <textarea
          name="description"
          class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
          required
          rows="8"></textarea>

        <div>
          <label for="price_network_buy_consumer" class="font-bold"
            >Price Network Buy Consumer:</label>
          <p class="text-sm text-gray-500">
            The price for buying energy from the energy provider
          </p>
        </div>

        <input
          step="any"
          type="number"
          name="price_network_buy_consumer"
          class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
          required />
        <div>
          <label for="price_network_sell_consumer" class="font-bold"
            >Price Network Sell Consumer:</label>
          <p class="text-sm text-gray-500">
            The price for selling energy back to the energy provider
          </p>
        </div>

        <input
          step="any"
          type="number"
          name="price_network_sell_consumer"
          class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
          required />
        <div>
          <label for="fixed_price_ratio" class="font-bold">Fixed Price Ratio:</label>
          <p class="text-sm text-gray-500">Determines the internal price for selling and buying energy. A higher ratio means that the price will tend towards the buying price</p>
        </div>

        <input
          step="any"
          type="number"
          name="fixed_price_ratio"
          class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600" />

        <div>
          <label for="costmodel_algorithm" class="font-bold">Costmodel Algorithm:</label>
          <p class="text-sm text-gray-500">A custom formula used to determine the internal buying and selling price. See documentation for details</p>
        </div>

        <div
          use:initMonaco={{
            initialCode: costmodelCode,
            onChange: (code) => (costmodelCode = code),
          }}
          class="h-48 border-2 border-gray-400 aria-selected:border-gray-600 rounded-lg">
        </div>

        {#if algorithmError}
          <p class="text-les-red">{algorithmError}</p>
        {/if}

        <button
          type="submit"
          class="py-3 bg-dark-les-bg rounded-lg text-white hover:bg-les-highlight transition-colors duration-200"
          >Submit</button>
      </form>
    {:else if currentStep === 3}
      <form method="post" on:submit|preventDefault={uploadAlgorithm} class="flex flex-col gap-6">
        <div>
          <label for="name" class="font-bold pt-4">Name:</label>
          <p class="text-sm text-gray-500">Name for the new algorithm</p>
        </div>

        <input
          type="text"
          name="name"
          class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
          required />

        <div>
          <label for="description" class="font-bold">Description:</label>
          <p class="text-sm text-gray-500">Description for the new algorithm</p>
        </div>

        <textarea
          name="description"
          class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
          required></textarea>

        <div>
          <label for="algorithm" class="font-bold">Algorithm:</label>
          <p class="text-sm text-gray-500">A custom algorithm used to determine when an appliance will be planned in. See documentation for details</p>
        </div>

        <div
          use:initMonaco={{
            initialCode: algorithmCode,
            onChange: (code) => (algorithmCode = code),
          }}
          class="h-48 border-2 border-gray-400 aria-selected:border-gray-600 rounded-lg">
        </div>

        <button
          type="submit"
          class="py-3 bg-dark-les-bg rounded-lg text-white hover:bg-les-highlight transition-colors duration-200"
          >Submit</button>
      </form>
    {/if}
  </div>
</div>
