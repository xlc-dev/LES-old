/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ApplianceTimeDailyRead } from "./ApplianceTimeDailyRead";
export type SelectedModelsOutput = {
  timedaily: Array<ApplianceTimeDailyRead>;
  // schedulable load grid kleuren
  results: Array<Array<number>>;
  // results: arrays in array. Elk heeft 4 getallen. Gebruiken voor de 4 grafieken
};
