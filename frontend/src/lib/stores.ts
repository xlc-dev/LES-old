import { writable } from "svelte/store";

import type { HouseholdRead } from "./client";

export const stepperData = writable(<Array<HouseholdRead>>[]);

export const twdata = writable({
  twin_world: '',
  cost_model: '',
  algorithm: ''
});
