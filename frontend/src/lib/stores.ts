import { type Writable, writable } from "svelte/store";

import type { HouseholdRead_Output, SelectedOptions } from "./client";

export const stepperData: Writable<SelectedOptions> = writable(<SelectedOptions>{
  algorithm: {},
  twinworld: {},
  costmodel: {},
  households: [],
});

export const activatedHousehold: Writable<HouseholdRead_Output> = writable(
  <HouseholdRead_Output>null
);

export interface EfficiencyResult {
  solarEnergyIndividual: number;
  solarEnergyTotal: number;
  internalBoughtEnergyPrice: number;
  totalAmountSaved: number;
}

function createRuntimeStore() {
  const { subscribe, set, update } = writable(0);
  let timer;

  return {
    subscribe,
    start: () => {
      set(0);
      timer = setInterval(() => {
        update((n) => Math.round((n + 0.01) * 100) / 100);
      }, 10);
    },
    stop: () => {
      clearInterval(timer);
    },
  };
}

export const efficiencyresultstore = writable<Array<EfficiencyResult>>([]);

export const isStarted = writable(false);

export const selectedDateStore = writable(new Date());

export const runtime = createRuntimeStore();

// new stores: efficiencyresultstore (4 graphs can be made with results:
// 1. % solar energy used by an individual household,
// 2. % total solar energy used by entire twin world full of household,
// 3. total price of internally (in local energy system) bought energy,
// 4. total amount saved),
// timedailystore
