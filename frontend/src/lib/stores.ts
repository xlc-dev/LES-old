import { writable } from "svelte/store";

import type { HouseholdRead } from "./client";

export const stepperData = writable(<Array<HouseholdRead>>[]);
