import { type Writable, writable } from "svelte/store";

import type { HouseholdRead_Output, SelectedOptions } from "./client";

export const stepperData: Writable<Array<HouseholdRead_Output>> = writable(<Array<HouseholdRead_Output>>[]);

export const activatedHousehold = writable(<HouseholdRead_Output>null);

export const twdata = writable({
  twinworld: "",
  costmodel: "",
  algorithm: "",
});
