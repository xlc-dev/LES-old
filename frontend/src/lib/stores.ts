import { type Writable, writable } from "svelte/store";

import type { HouseholdRead_Output, SelectedOptions } from "./client";

export const stepperData: Writable<SelectedOptions> = writable(<SelectedOptions>{algorithm: {}, twinworld: {}, costmodel: {}, households: []});

export const activatedHousehold: Writable<HouseholdRead_Output> = writable(
  <HouseholdRead_Output>null
);

// new stores: efficiencyresultstore (4 graphs can be made with results:
// 1. % solar energy used by an individual household,
// 2. % total solar energy used by entire twin world full of household,
// 3. total price of internally (in local energy system) bought energy,
// 4. total amount saved),
// timedailystore
