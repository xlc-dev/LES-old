<script lang="ts">
  /*
   * The stepper component contains the first views the researcher is presented with.
   * The stepper can be seen as a setup wizard for a single session of using the application
   * and consists of three steps which the researcher goes through to prepare the environment
   * in which research is conducted. A pre-built twin world, cost model, and algorithm must be
   * selected or created as custom options in order for the environment to be created.
   */

  import { onMount } from "svelte";
  import { fade } from "svelte/transition";

  import * as monaco from "monaco-editor";

  import { isStarted, stepperData } from "../lib/stores";
  import { message } from "../lib/message";

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
    EnergyflowService,
    OpenAPI,
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
    twinworld: [],
    costmodel: [],
    energyflow: [],
  };

  let selectedIDs = {
    twinworld: 0,
    costmodel: 0,
    algorithm: 0,
    energyflow: 0,
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

  let costmodelCode = "return buy_consumer * ratio + sell_consumer * (1 - ratio)";
  let algorithmCode =
    "import pandas\nimport numpy\nimport scipy\nimport math\nimport random\n\ndef run():\n    pass\n";

  let checkboxStates = Array(24).fill(false);
  let currentStep: number = 0;
  let isStepZero: boolean = true;

  let currentDescription: string = "";
  let currentAppliances: ApplianceRead_Output[] = null;

  let applianceToAdd: number = 0;
  let timewindowToAdd: number = 0;

  let twinworldHouseholds = [];

  let applianceCheck: Array<{
    householdName: string;
    noAppliance: boolean;
    appliance?: string;
    missingDay?: ApplianceDays;
  }> = [];

  let editingHousehold: HouseholdRead_Output = null;
  let editingApplianceTimeWindow: ApplianceTimeWindowRead = null;

  /**
   * Updates the value of the description frame, based on the hovered option in the options frame.
   * @param {string} description - The set description for the item.
   * @returns {void}
   */
  const updateDescription = (description: string) => {
    currentDescription = description;
  };

  /**
   * Loads elements for editing a household in a created twin world.
   * @param {HouseholdRead_Output} household - The household object to be edited.
   * @returns {void}
   */
  const startEditingHousehold = (household: HouseholdRead_Output) => {
    editingHousehold = household;
  };

  /**
   * Loads elements for editing time slots for a created household.
   * @param {ApplianceTimeWindowRead} timewindow - The ApplianceTimeWindowRead object to set the value to.
   * @returns {void}
   */
  const startEditingTimewindow = (timewindow: ApplianceTimeWindowRead) => {
    editingApplianceTimeWindow = timewindow;
  };

  /**
   * Automatically scrolls the screen to the next appliance element when adding appliances for a created household.
   * @returns {void}
   */
  const scrollToApplianceLocation = () => {
    const applianceLocation = document.getElementById("applianceLocation");
    if (applianceLocation) {
      applianceLocation.scrollIntoView({ behavior: "smooth" });
    }
  };

  /**
   * Automatically scrolls the screen to the next time slot element when adding time slots for a created household.
   * @returns {void}
   */
  const scrollToTimewindowLocation = () => {
    const applianceLocation = document.getElementById("timewindowLocation");
    if (applianceLocation) {
      applianceLocation.scrollIntoView({ behavior: "smooth" });
    }
  };

  /**
   * Applies the selected time ranges and converts them to usable bitmap values
   * @returns {void}
   */
  const updateBitmapWindow = () => {
    newTimeWindow.bitmap_window = checkboxStates.reduce((acc, state: any, index) => {
      return acc | (state << index);
    }, 0);
  };

  /**
   * Updates the descriptions in the descriptions frame for the current step.
   * @returns {void}
   */
  const updateDescriptionForCurrentStep = () => {
    const keys = Object.keys(simulationData);
    if (currentStep > 0 && currentStep <= keys.length) {
      const key = keys[currentStep - 1];
      currentDescription =
        simulationData[key] && simulationData[key][0] ? simulationData[key][0].description : "";
    } else {
      currentDescription = "";
    }
  };

  /**
   * Updates the state of the stepper by loading the view of the next step in the stepper.
   * @async
   * @returns {void}
   */
  const nextStep = async () => {
    if (isStepZero) {
      isStepZero = false;
      currentStep = 1;
      updateDescriptionForCurrentStep();
      return;
    }

    const keys = Object.keys(simulationData) as (keyof SimulationData)[];

    if (currentStep === 4) {
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

  /**
   * Updates the state of the stepper by loading the view of the previous step in the stepper.
   * @returns {void}
   */
  const prevStep = () => {
    const keys = Object.keys(simulationData) as (keyof SimulationData)[];
    if (currentStep > 1) {
      currentStep -= 1;
      currentDescription = simulationData[keys[currentStep - 1]][0]?.description || "";
    }
  };

  /**
   * Checks if a step is completed by determining whether all required actions within the step are run and no errors occur.
   * @param {number} step - The step number to check.
   * @returns {boolean} - Returns true if the step is completed, otherwise false.
   */
  const isStepCompleted = (step: number): boolean => {
    const keys = Object.keys(selectedIDs) as (keyof typeof selectedIDs)[];
    const currentStepKey = keys[step - 1];
    return selectedIDs[currentStepKey] !== 0;
  };

  /**
   * Updates the state of the stepper by loading the view of a specifically selected step in the stepper.
   * @param {number} stepNumber - The step number to go to.
   * @returns {void}
   */
  const goToStep = (stepNumber: number) => {
    currentStep = stepNumber;
    currentDescription =
      simulationData[Object.keys(simulationData)[currentStep - 1]][0]?.description || "";
  };

  /**
   * Handles a button click when an option in the options frame has been selected.
   * @param {number} optionId - The ID of the option to be selected.
   * @param {string} category - The category to which the option belongs.
   * @param {string} optionName - The name of the option.
   * @returns {void}
   */
  const selectOption = (optionId: number, category: string, optionName: string) => {
    selectedIDs[category] = optionId;
    stepperData.update((data) => ({ ...data, [category]: optionName }));
    if (category === "twinworld") {
      fetchHouseholds();
    }
  };

  /**
   * Removes an option in the options frame that has been created by the researcher.
   * @param {number} optionId - The ID of the option to be deleted.
   * @param {any} category - The category of the option.
   * @async
   * @returns {void}
   */
  const deleteOption = async (optionId: number, category: any) => {
    selectedIDs[category] = 0;
    stepperData.update((data) => ({ ...data, [category]: "-" }));
    await deleteOptionBasedOnCategory(category, optionId);
    simulationData = await SimulateService.getDataApiSimulateLoadDataGet();
    message(`${category} deleted`);
  };

  /**
   * Removes an option in the options frame that has been created by the researcher based on a category.
   * @param {keyof SimulationData} category - The category of the option to be deleted.
   * @param {number} optionId - The ID of the option to be deleted.
   * @async
   * @returns {Promise<void>} - A Promise that resolves with no value.
   */
  const deleteOptionBasedOnCategory = async (category: keyof SimulationData, optionId: number) => {
    switch (category) {
      case "costmodel":
        await CostModelService.deleteCostmodelApiCostmodelIdDelete(optionId);
        break;
      case "twinworld":
        await TwinWorldService.deleteTwinworldApiTwinworldIdDelete(optionId);
        break;
      case "algorithm":
        await AlgorithmService.deleteAlgorithmApiAlgorithmIdDelete(optionId);
        break;
      case "energyflow":
        await EnergyflowService.deleteEnergyflowApiEnergyflowIdDelete(optionId);
        break;
      default:
        break;
    }

    updateDescriptionForCurrentStep();
  };

  /**
   * Initializes the Monaco editor for the custom algorithms in the cost model step of the stepper.
   * @param {HTMLElement} node - The HTML element to attach the editor to.
   * @param {Object} options - The options for configuring the editor.
   * @param {string} options.initialCode - The initial code to display in the editor.
   * @param {Function} options.onChange - The callback function to be executed when the code in the editor changes.
   * @returns {Object} An object with methods to update and destroy the editor.
   */
  const initMonaco = (node: HTMLElement, { initialCode, onChange }) => {
    const editor = monaco.editor.create(node, {
      value: initialCode,
      language: "python",
      lineNumbers: "on",
      automaticLayout: true,
    });

    /**
     * Updates the state of the Monaco editor when changes in the provided code are detected.
     * @returns {void}
     */
    const handleEditorChange = () => {
      const newValue = editor.getValue();
      onChange(newValue);
      monaco.editor.setModelMarkers(editor.getModel(), "python", []);
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

  /**
   * Assigns time slots and appliances to a created schedulable load.
   * @async
   * @returns {Promise<void>} - A Promise that resolves with no value.
   */
  const addTimewindow = async () => {
    if (checkboxStates.every((state) => state === false)) {
      message("Please select at least one hour");
      return;
    }

    if (newTimeWindow.appliance_id === 0) {
      message("Please select at least one appliance");
      return;
    }

    await ApplianceService.postApplianceTimewindowApiApplianceTimewindowPost(newTimeWindow)
      .then(async () => {
        twinworldHouseholds =
          await HouseholdService.getHouseholdsByTwinworldApiHouseholdTwinworldTwinworldIdGet(
            selectedIDs.twinworld
          );

        checkboxStates = Array(24).fill(false);
        message("Time window added");
      })
      .catch((err) => {
        message(err);
      });
  };

  /**
   * Removes a created schedulable load.
   * @param {number} id - The ID of the time window to delete.
   * @async
   * @returns {Promise<void>} - A Promise that resolves with no value.
   * @throws {Error} - If an error occurs while deleting the time window.
   */
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

      message("Time window deleted");
    } catch (err) {
      message(err);
    }
  };

  /**
   * Discards elements of time slots that were being edited for a created household.
   * or an error message if there is an exception.
   * @async
   * @returns {void}
   */
  const stopEditingTimewindow = async () => {
    try {
      await ApplianceService.updateApplianceTimewindowApiApplianceTimewindowIdPatch(
        editingApplianceTimeWindow.id,
        editingApplianceTimeWindow
      );
      editingApplianceTimeWindow = null;
      message("Time window updated");
    } catch (err) {
      message(err);
    }
  };

  /**
   * Adds an appliance to a created household.
   * @async
   * @returns {Promise<void>} A Promise that resolves with no value.
   */
  const addAppliance = async () => {
    newAppliance.household_id = applianceToAdd;
    await ApplianceService.postApplianceApiAppliancePost(newAppliance)
      .then(async () => {
        twinworldHouseholds =
          await HouseholdService.getHouseholdsByTwinworldApiHouseholdTwinworldTwinworldIdGet(
            selectedIDs.twinworld
          );

        applianceToAdd = 0;
        message("Appliance added");
      })
      .catch((err) => {
        message(err);
      });
  };

  /**
   * Removes an appliance from a created household.
   * @async
   * @param {number} id - The ID of the appliance to be deleted.
   * @returns {Promise<void>} - A Promise that resolves with no value.
   */
  const deleteAppliance = async (id: number) => {
    try {
      await ApplianceService.deleteApplianceApiApplianceIdDelete(id);

      twinworldHouseholds = twinworldHouseholds.map((household) => {
        household.appliances = household.appliances.filter(
          (appliance: ApplianceRead_Output) => appliance.id !== id
        );
        return household; // return so svelte can update the array
      });
      message("Appliance deleted");
    } catch (err) {
      message(err);
    }
  };

  /**
   * Adds a household to a created twin world.
   * @async
   * @returns {Promise<void>} A Promise that resolves with no value.
   * @throws {Error} If there was an error while adding the household.
   */
  const addHousehold = async () => {
    newHousehold.twinworld_id = selectedIDs.twinworld;
    await HouseholdService.postHouseholdApiHouseholdPost(newHousehold)
      .then(async () => {
        twinworldHouseholds =
          await HouseholdService.getHouseholdsByTwinworldApiHouseholdTwinworldTwinworldIdGet(
            selectedIDs.twinworld
          );

        twinworldHouseholds = twinworldHouseholds;
        applianceToAdd = 0;
        message("Household added");
      })
      .catch((err) => {
        message(err);
      });
  };

  /**
   * Removes a household from a created twin world.
   * @async
   * @param {number} id - The ID of the household to delete.
   * @returns {Promise} - A Promise that resolves when the household is deleted or rejects with an error.
   */
  const deleteHousehold = async (id: number) => {
    await HouseholdService.deleteHouseholdApiHouseholdIdDelete(id)
      .then(() => {
        twinworldHouseholds = twinworldHouseholds.filter((household) => household.id !== id);
        message("Household deleted");
      })
      .catch((err) => {
        message(err);
      });
  };

  /**
   * Discards elements of a household that was being edited for a created twin world.
   * @async
   * @returns {Promise<void>} A promise that resolves when the household is updated or rejects with an error.
   */
  const stopEditingHousehold = async () => {
    try {
      await HouseholdService.updateHouseholdApiHouseholdIdPatch(
        editingHousehold.id,
        editingHousehold
      );
      editingHousehold = null;
      message("Household updated");
    } catch (err) {
      message(err);
    }
  };

  /**
   * Fetches all households for the selected twin world.
   * @async
   * @returns {Promise} - A Promise that resolves with the fetched households.
   */
  const fetchHouseholds = async () => {
    if (selectedIDs.twinworld) {
      twinworldHouseholds =
        await HouseholdService.getHouseholdsByTwinworldApiHouseholdTwinworldTwinworldIdGet(
          selectedIDs.twinworld
        );
    }
  };

  /**
   * Sends a post request containing the form data of a created energy flow and add it to the array of selectable options.
   * @param {any} event - The event object containing the target element.
   * @async
   * @returns {Promise<void>} - A promise that resolves when the energy flow is successfully uploaded.
   */
  const uploadEnergyFlow = async ({ target }) => {
    const formData = new FormData();
    formData.append("name", target.name.value);
    formData.append("description", target.description.value);
    formData.append("solar_panels_factor", target.solar_panels_factor.value);
    formData.append("energy_usage_factor", target.energy_usage_factor.value);
    formData.append("file", target.file.files[0]);

    const response = await fetch(OpenAPI.BASE + "/api/energyflow/upload", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      message(response.statusText);
      return;
    }

    message("Energyflow uploaded");
    simulationData = await SimulateService.getDataApiSimulateLoadDataGet();
  };

  /**
   * Sends a post request containing the form data of a created cost model and add it to the array of selectable options.
   * @param {any} event - The event object containing the target element.
   * @async
   * @returns {Promise<void>} - A promise that resolves when the cost model is successfully uploaded.
   */
  const uploadCostModel = async ({ target }) => {
    const formData = {
      name: target.name.value,
      description: target.description.value,
      price_network_buy_consumer: target.price_network_buy_consumer.value,
      price_network_sell_consumer: target.price_network_sell_consumer.value,
      fixed_price_ratio: target.fixed_price_ratio.value,
      algorithm: costmodelCode,
    };

    try {
      await CostModelService.postCostmodelApiCostmodelPost(formData);
      simulationData = await SimulateService.getDataApiSimulateLoadDataGet();
      selectedIDs.costmodel = simulationData.costmodel[simulationData.costmodel.length - 1].id;
      $stepperData.costmodel = target.name.value;
      window.scrollTo({ top: 0, behavior: "smooth" });
      message("Cost model created");
    } catch (err) {
      message(err);
    }
  };

  /**
   * Sends a post request to save a created twin world and add it to the array of selectable options.
   * @param {any} event - The event object that triggered the upload.
   * @async
   * @returns {void}
   */
  const uploadTwinWorld = async ({ target }) => {
    const formData = {
      name: target.name.value,
      description: target.description.value,
    };

    try {
      await TwinWorldService.postTwinworldApiTwinworldPost(formData);
      simulationData = await SimulateService.getDataApiSimulateLoadDataGet();
      twinworldHouseholds = [];
      selectedIDs.twinworld = simulationData.twinworld[simulationData.twinworld.length - 1].id;
      fetchHouseholds(); // Fetch households for the newly created twin world
      message("Twin world created");
    } catch (err) {
      message(err);
    }
  };

  /**
   * Sends a post request to save a created algorithm and add it to the array of selectable options.
   * @param {any} event - The event data.
   * @async
   * @returns {Promise<void>} - A promise that resolves once the algorithm is uploaded.
   */
  const uploadAlgorithm = async (event: any) => {
    const target = event.target;

    const formData = {
      name: target.name.value,
      description: target.description.value,
      max_temperature: target.max_temperature.value,
      algorithm: algorithmCode,
    };

    try {
      await AlgorithmService.postAlgorithmApiAlgorithmPost(formData);
      simulationData = await SimulateService.getDataApiSimulateLoadDataGet();
      selectedIDs.algorithm = simulationData.algorithm[simulationData.algorithm.length - 1].id;
      window.scrollTo({ top: 0, behavior: "smooth" });
      $stepperData.algorithm = target.name.value;
      message("Algorithm created");
    } catch (err) {
      message(err);
    }
  };

  /**
   * Processes all the selected options that were selected in the stepper and starts a simulation if the data is valid.
   * @async
   * @returns {undefined}
   */
  const startSimulation = async () => {
    applianceCheck = [];
    const hasApplianceWithoutEveryDay = twinworldHouseholds
      .map((household) => {
        // Check if the household has appliances
        if (!household.appliances || household.appliances.length === 0) {
          applianceCheck.push({
            householdName: household.name,
            noAppliance: true,
          });
          return true; // Return true to indicate no appliances
        }

        return household.appliances.map((appliance: ApplianceRead_Output) => {
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
                  noAppliance: false,
                  appliance: appliance.name,
                  missingDay: day,
                });
              });
            }

            return missingDays.length > 0; // Return true if missingDays is not empty
          }

          return false; // Return false if appliance_windows is undefined or null
        });
      })
      .flat()
      .some(Boolean);

    if (hasApplianceWithoutEveryDay) {
      applianceCheck.map((check) => {
        if (check.noAppliance) {
          message(check.householdName + " has no appliances.");
        } else {
          message(
            check.householdName + " is missing " + check.missingDay + " for " + check.appliance
          );
        }
      });
      goToStep(1);
      return; // Don't continue with the function if there are appliances without every day or no appliances
    }

    await SimulateService.startApiSimulateStartPost({
      algorithm_id: selectedIDs.algorithm,
      twinworld_id: selectedIDs.twinworld,
      costmodel_id: selectedIDs.costmodel,
      energyflow_id: selectedIDs.energyflow,
    })
      .then((res) => {
        $stepperData = res;
        $isStarted = true;
      })
      .catch((err) => {
        message(err);
      });
  };

  /*
   * Contains logic that runs at initialisation, as soon as the component has been mounted.
   * In this component it initialises the simulation data, the twin world, the simulation data's object keys, and the Monaco editors.
   */
  onMount(async () => {
    simulationData = await SimulateService.getDataApiSimulateLoadDataGet();

    const keys = Object.keys(simulationData) as (keyof SimulationData)[];
    if (keys.length > 0) {
      currentDescription = simulationData[keys[0]][0]?.description || "";
    }
  });

  /**
   * If an appliance has been added to a created twin world the window scrolls to a section in which a new appliance can be added.
   * @param {number} applianceToAdd - Number of appliances to add.
   */
  $: if (applianceToAdd > 0) {
    setTimeout(() => {
      scrollToApplianceLocation();
    }, 100);
  }

  /**
   * Adds the created appliances for a specific created household.
   * @param {number} timewindowToAdd - The id of the timewindow.
   */
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

  /**
   * Updates the description for the current step if the step number is not zero.
   * @param {boolean} isStepZero - Indicates whether the current step number is zero.
   * @returns {void}
   */
  $: if (!isStepZero) {
    updateDescriptionForCurrentStep();
  }
</script>

<div class="max-w-3xl mx-auto pt-8">
  {#if !isStepZero}
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
                class={`absolute top-4 left-8 border-t-2 w-[13.3rem] transition-colors duration-200 ${
                  isStepCompleted(index + 1) ? "border-les-blue" : "border-gray-300"
                }`}>
              </div>
            {/if}

            <p class="text-white absolute top-10 transform -translate-x-28 w-64 text-center">
              {#if selectedIDs.twinworld !== 0 && stepName === "twinworld"}
                {#if applianceCheck.length > 0}
                  <span class="!text-les-red">{$stepperData.twinworld}</span>
                {:else}
                  {$stepperData.twinworld}
                {/if}
              {:else if selectedIDs.costmodel !== 0 && stepName === "costmodel"}
                {$stepperData.costmodel}
              {:else if selectedIDs.algorithm !== 0 && stepName === "algorithm"}
                {$stepperData.algorithm}
              {:else if selectedIDs.energyflow !== 0 && stepName === "energyflow"}
                {$stepperData.energyflow}
              {:else}
                -
              {/if}
            </p>
          </div>
        {/each}
      {/key}
    </div>
  {/if}

  {#if isStepZero}
    <div class="mx-auto pt-8">
      <img src="/favicon.png" class="w-48 mx-auto rounded-lg" alt="LES Logo" />
      <h1 class="font-bold text-4xl text-center text-white pt-4">
        Local Energy System Simulation
      </h1>
      <p class="text-lg text-center py-4 text-white">
        Welcome to the LES Research application. You can determine the efficiency of algorithms and
        cost models by creating your own simulations. Please continue with the following steps to
        set up the environment you would like to research.
      </p>
      <button
        on:click={nextStep}
        class="block w-full py-3 rounded-lg text-white transition duration-200 bg-les-blue hover:brightness-110"
        >Get started</button>
    </div>
  {:else}
    {#each Object.keys(simulationData) as key, index (key)}
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

                      {#if (option.name !== "energyflow" && option.id !== 1 && option.id !== 2) || (option.name === "energyflow" && option.id !== 1)}
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
          <div class="flex justify-between mt-8 relative">
            {#if currentStep !== 1}
              <button
                class="px-6 py-3 rounded-lg text-white transition-colors duration-200 bg-les-highlight hover:bg-dark-les-bg"
                on:click={prevStep}
                >Back
              </button>
            {/if}

            {#if selectedIDs.algorithm !== 0 && selectedIDs.twinworld !== 0 && selectedIDs.costmodel !== 0 && selectedIDs.energyflow !== 0}
              <button
                class="{currentStep === 4
                  ? 'ml-auto'
                  : 'absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2'} px-6 py-3 rounded-lg text-white transition-colors duration-200 bg-les-red hover:brightness-110"
                on:click={startSimulation}>
                Start
              </button>
            {/if}

            {#if currentStep !== 4}
              <button
                class="px-6 py-3 rounded-lg text-white transition-colors duration-200 bg-les-blue hover:brightness-110 ml-auto"
                on:click={nextStep}
                >Next
              </button>
            {/if}
          </div>
        </div>
      {/if}
    {/each}
  {/if}

  {#if !isStepZero && simulationData && Object.keys(simulationData).length > 0}
    <div class="mt-8 bg-white rounded-lg p-4 mb-8 border-4 border-gray-400 shadow">
      <p class="font-bold text-lg mb-4">
        Upload Custom {Object.keys(simulationData)[currentStep - 1].charAt(0).toUpperCase() +
          Object.keys(simulationData)[currentStep - 1].slice(1).replace("_", " ")}:
      </p>

      {#if currentStep === 1}
        <form
          method="post"
          on:submit|preventDefault={uploadTwinWorld}
          class="flex flex-col space-y-3">
          <div>
            <label for="name" class="font-bold pt-4">Name:</label>
            <p class="text-sm text-gray-500">Name of the twinworld</p>
          </div>

          <input
            type="text"
            name="name"
            class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
            placeholder="Custom Twinworld"
            required />

          <div>
            <label for="description" class="font-bold">Description:</label>
            <p class="text-sm text-gray-500">Description of the twinworld</p>
          </div>

          <textarea
            name="description"
            class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
            placeholder="My own twinworld"
            required></textarea>

          <button
            type="submit"
            class="py-3 bg-dark-les-bg rounded-lg text-white hover:bg-les-highlight transition-colors duration-200"
            >Submit
          </button>
        </form>

        {#if selectedIDs.twinworld && selectedIDs.twinworld !== 1 && selectedIDs.twinworld !== 2}
          <hr class="my-8 bg-les-highlight" />

          <h2 class="font-bold text-lg mb-4">
            Add household for Twin World: {$stepperData.twinworld}
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
                placeholder="Household 10" />
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
                placeholder="3100" />
            </div>

            <div class="flex flex-col w-full sm:w-1/2 md:w-1/3 pr-4">
              <label for="solar_panels" class="font-bold">Solar Panels:</label>
              <input
                id="solar_panels"
                class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
                type="number"
                min="0"
                bind:value={newHousehold.solar_panels}
                placeholder="10" />
            </div>

            <div class="flex flex-col w-full sm:w-1/2 md:w-1/3 pr-4">
              <label for="solar_yield_yearly" class="font-bold">Solar Yield Yearly:</label>
              <input
                id="solar_yield_yearly"
                class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
                type="number"
                min="0"
                bind:value={newHousehold.solar_yield_yearly}
                placeholder="3400" />
            </div>
            <div class="flex items-end">
              <button
                type="button"
                class="py-3 px-4 bg-dark-les-bg rounded-lg text-white hover:bg-les-highlight transition-colors duration-200"
                on:click={addHousehold}
                >Add Household
              </button>
            </div>
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
                  step="0.01"
                  min="0.01"
                  bind:value={newAppliance.power} />
              </div>

              <div class="flex flex-col w-full sm:w-1/2 md:w-1/3 pr-4">
                <label for="duration" class="font-bold">Duration:</label>
                <input
                  id="duration"
                  class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
                  type="number"
                  step="1"
                  min="1"
                  max="24"
                  bind:value={newAppliance.duration} />
              </div>

              <div class="flex flex-col w-full sm:w-1/2 md:w-1/3 pr-4">
                <label for="daily_usage" class="font-bold">Daily Usage:</label>
                <input
                  id="daily_usage"
                  class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
                  type="number"
                  step="0.01"
                  min="0.01"
                  bind:value={newAppliance.daily_usage} />
              </div>

              <div class="flex items-end">
                <button
                  type="button"
                  class="py-3 px-4 bg-dark-les-bg rounded-lg text-white hover:bg-les-highlight transition-colors duration-200"
                  on:click={addAppliance}
                  >Add Appliance
                </button>
              </div>
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
                        >Day
                      </th>
                      <th
                        class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs text-gray-600 uppercase tracking-wider"
                        >Bitmap Window
                      </th>
                      <th
                        class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs text-gray-600 uppercase tracking-wider"
                        >Options
                      </th>
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
                  on:click={addTimewindow}
                  >Add Timewindow
                </button>
              </div>
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
                    >Name
                  </th>

                  <th
                    class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs text-gray-600 uppercase tracking-wider"
                    >Size
                  </th>
                  <th
                    class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs text-gray-600 uppercase tracking-wider"
                    >Energy Usage
                  </th>

                  <th
                    class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs text-gray-600 uppercase tracking-wider"
                    >Solar Yield Yearly
                  </th>

                  <th
                    class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs text-gray-600 uppercase tracking-wider"
                    >Appliances
                  </th>

                  <th
                    class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs text-gray-600 uppercase tracking-wider"
                    >Options
                  </th>
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
            placeholder="custom Costmodel"
            required />

          <div>
            <label for="description" class="font-bold">Description:</label>
            <p class="text-sm text-gray-500">Description of the costmodel</p>
          </div>

          <textarea
            name="description"
            class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
            required
            placeholder="My own costmodel"
            rows="8"></textarea>

          <div>
            <label for="price_network_buy_consumer" class="font-bold"
              >Price Network Buy Consumer:</label>
            <p class="text-sm text-gray-500">
              The price for buying energy from the energy provider
            </p>
          </div>

          <input
            step="0.1"
            type="number"
            name="price_network_buy_consumer"
            class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
            placeholder="0.4"
            required />

          <div>
            <label for="price_network_sell_consumer" class="font-bold"
              >Price Network Sell Consumer:</label>
            <p class="text-sm text-gray-500">
              The price for selling energy back to the energy provider
            </p>
          </div>

          <input
            step="0.1"
            type="number"
            name="price_network_sell_consumer"
            class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
            placeholder="0.1"
            required />

          <div>
            <label for="fixed_price_ratio" class="font-bold">Fixed Price Ratio:</label>
            <p class="text-sm text-gray-500">
              Determines the internal price for selling and buying energy. A higher ratio means
              that the price will tend towards the buying price
            </p>
          </div>

          <input
            step="0.1"
            type="number"
            name="fixed_price_ratio"
            placeholder="0.5"
            class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600" />

          <div>
            <label for="algorithm" class="font-bold">Costmodel Algorithm:</label>
            <p class="text-sm text-gray-500">
              A custom formula used to determine the internal buying and selling price. See
              documentation for details
            </p>
          </div>

          <div
            use:initMonaco={{
              initialCode: costmodelCode,
              onChange: (code) => (costmodelCode = code),
            }}
            class="h-48 border-2 border-gray-400 aria-selected:border-gray-600 rounded-lg">
          </div>

          <button
            type="submit"
            class="py-3 bg-dark-les-bg rounded-lg text-white hover:bg-les-highlight transition-colors duration-200"
            >Submit
          </button>
        </form>
      {:else if currentStep === 3}
        <form
          method="post"
          on:submit|preventDefault={uploadAlgorithm}
          class="flex flex-col space-y-3">
          <div>
            <label for="name" class="font-bold pt-4">Name:</label>
            <p class="text-sm text-gray-500">Name for the new algorithm</p>
          </div>

          <input
            type="text"
            name="name"
            class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
            placeholder="Custom Algorithm"
            required />

          <div>
            <label for="description" class="font-bold">Description:</label>
            <p class="text-sm text-gray-500">Description for the new algorithm</p>
          </div>

          <textarea
            name="description"
            class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
            placeholder="My own algorithm"
            required></textarea>

          <div>
            <label for="description" class="font-bold">Max Temperature:</label>
            <p class="text-sm text-gray-500">Set the max temperature for your algorithm</p>
          </div>

          <input
            step="any"
            type="number"
            name="max_temperature"
            class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
            placeholder="10000" />

          <div>
            <label for="algorithm" class="font-bold">Algorithm:</label>
            <p class="text-sm text-gray-500">
              A custom algorithm used to determine when an appliance will be planned in. See
              documentation for details
            </p>
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
            >Submit
          </button>
        </form>
      {:else if currentStep === 4}
        <form
          method="post"
          enctype="multipart/form-data"
          on:submit|preventDefault={uploadEnergyFlow}
          class="flex flex-col space-y-3">
          <div>
            <label for="name" class="font-bold pt-4">Name:</label>
            <p class="text-sm text-gray-500">Name for the new energy flow</p>
          </div>

          <input
            type="text"
            name="name"
            class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
            placeholder="Custom energy flow"
            required />

          <div>
            <label for="description" class="font-bold">Description:</label>
            <p class="text-sm text-gray-500">Description for the new energy flow</p>
          </div>

          <textarea
            name="description"
            class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
            placeholder="My own energy flow data"
            required></textarea>

          <div>
            <label for="solar_panels_factor" class="font-bold pt-4">Solar Panels Factor:</label>
            <p class="text-sm text-gray-500">
              Amount of solar panels for the household in the supplied energy table
            </p>
          </div>

          <input
            type="number"
            name="solar_panels_factor"
            class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
            step="1"
            min="1"
            placeholder="25"
            required />

          <div>
            <label for="energy_usage_factor" class="font-bold pt-4">Energy Usage Factor:</label>
            <p class="text-sm text-gray-500">
              Amount of yearly energy used for the household in the supplied energy table
            </p>
          </div>

          <input
            type="number"
            name="energy_usage_factor"
            class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
            step="1"
            min="1"
            placeholder="7000"
            required />

          <div>
            <label for="file" class="font-bold">File:</label>
            <p class="text-sm text-gray-500">CSV file for Energyflow</p>
          </div>

          <input
            type="file"
            name="file"
            accept=".csv"
            class="bg-les-white p-3 rounded-lg border-2 border-gray-400 aria-selected:border-gray-600"
            required />

          <button
            type="submit"
            class="py-3 bg-dark-les-bg rounded-lg text-white hover:bg-les-highlight transition-colors duration-200"
            >Submit
          </button>
        </form>
      {/if}
    </div>
  {/if}
</div>
