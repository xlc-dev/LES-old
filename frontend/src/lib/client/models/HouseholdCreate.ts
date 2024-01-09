/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ApplianceCreate } from "./ApplianceCreate";

export type HouseholdCreate = {
  name: string;
  size?: number;
  energy_usage: number;
  solar_panels?: number;
  solar_yield_yearly: number;
  appliances?: Array<ApplianceCreate>;
};
