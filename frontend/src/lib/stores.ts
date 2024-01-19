import { type Writable, writable } from "svelte/store";

import type { HouseholdRead_Output, SelectedOptions } from "./client";

export const stepperData: Writable<SelectedOptions> = writable(<SelectedOptions>{algorithm: {}, twinworld: {}, costmodel: {}, households: []});

export const activatedHousehold: Writable<HouseholdRead_Output> = writable(
  <HouseholdRead_Output>null
);

// new stores: bitmapefficiencyresultstore (4 grafieken te maken met results), timedailystore
