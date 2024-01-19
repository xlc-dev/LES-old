import { writable } from "svelte/store";

import type { HouseholdRead_Output } from "./client";

export const stepperData = writable(<Array<HouseholdRead_Output>>[]);

export const activatedHousehold = writable(<HouseholdRead_Output>null);

export const twdata = writable({
  twin_world: "",
  cost_model: "",
  algorithm: "",
});
