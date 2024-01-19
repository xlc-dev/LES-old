/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ApplianceTimeDailyRead } from "./ApplianceTimeDailyRead";
export type SelectedModelsOutput = {
  // schedulable load grid colours
  timedaily: Array<ApplianceTimeDailyRead>;

  // results: arrays in array. Each contains 4 numbers. Use this for the 4 graphs.
  results: Array<Array<number>>;
};
