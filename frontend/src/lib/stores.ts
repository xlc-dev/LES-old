import {
  type Invalidator,
  type Subscriber,
  type Unsubscriber,
  type Writable,
  writable,
} from "svelte/store";

import type { HouseholdRead_Output, SelectedOptions, ApplianceTimeDailyRead } from "./client";

export interface EfficiencyResult {
  solarEnergyIndividual: number;
  solarEnergyTotal: number;
  internalBoughtEnergyPrice: number;
  totalAmountSaved: number;
}

const createRuntimeStore = () => {
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
};

export const runtime: {
  stop: () => void;
  subscribe: (
    this: void,
    run: Subscriber<number>,
    invalidate?: Invalidator<number>
  ) => Unsubscriber;
  start: () => void;
} = createRuntimeStore();

export const stepperData: Writable<SelectedOptions> = writable(<SelectedOptions>{
  algorithm: {},
  twinworld: {},
  costmodel: {},
  energyflow: {},
  households: [],
});

export const activatedHousehold: Writable<HouseholdRead_Output> = writable(
  <HouseholdRead_Output>null
);

export const efficiencyresultstore = writable<Array<EfficiencyResult>>([]);

export const timeDailies = writable<Array<ApplianceTimeDailyRead>>([]);

export const messages = writable<Array<{ id: number; msg: string }>>([]);

export const startDate = writable(0);
export const endDate = writable(0);

export const isStarted = writable(false);
